$(document).ready(function() {
    $("#submitButton").click(function(e) {
        e.preventDefault();

        var productName = $("#itemName").val();
        console.log(productName)
        $.ajax({
            url: "/text_inference",
            type: "POST",
            data: { product_name: productName },
            success: function(response) {
                console.log(response)
                calculateTax(response);
            },
            error: function(xhr, status, error) {
                console.error("Error generating product type:", error);
                alert('Error generating product type.');
            }
        });
    });

    function calculateTax(productType) {
        var formData = $("#taxForm").serialize();
        formData += "&product_type=" + encodeURIComponent(productType);
        const formParams = new URLSearchParams(formData);
        console.log(formData)
        $.ajax({
            url: "/tax_inference",
            type: "POST",
            data: formData,
            success: function(response) {
                if (response.error) {
                    $("#taxResult").html("Error: " + response.error);
                } else {
                    $.getJSON("/static/basic_rates.json", function(basicRates) {
                        // Correct selector for the select element
                        var state = formParams.get("state");
                        state = state.charAt(0).toUpperCase() + state.substring(1).toLowerCase()
                        const std_rate = parseFloat(basicRates[state]) * 100.0;
                        const tax_rate = parseFloat(response.tax_rate);
                        var pretax_price = parseFloat(formParams.get("price")) * parseFloat(formParams.get("quantity"))
                        var total_tax = parseFloat(response.total_tax)
                        var final_price = pretax_price + total_tax
                        const thold = 1.0;
                        console.log("STD RATE: " + std_rate + ", TAX RATE: " + tax_rate);

                        $(".type_name_result").text(productType)
                        $(".tax_rate").text(response.tax_rate + "%")
                        $(".final_price").text("$" + final_price.toFixed(2))
                        $(".percentage").text("$" + total_tax.toFixed(2))
                        $(".in_tax").text(" taxed")
                        if (std_rate - tax_rate > thold) {
                            $(".extra_note").text("Note: Tax rates for " + state + " may have tax exemptions or reduced-rate for this product type")
                        } else if (tax_rate - std_rate > thold) {
                            $(".extra_note").text("Note: Tax rates for " + state + " may have tax-liabilities for this product type")
                        }
                    })
                    .fail(function(jqxhr, textStatus, error) {
                        console.error("Error fetching basic_rates.json:", textStatus, error);
                        $("#taxResult").html("Error: Could not fetch tax rates.");
                    });
                }
                success = saveCalculation(response, productType)
                $("#taxForm")[0].reset(); // Clear the form
            },
            error: function(xhr, status, error) {
                console.error("Error calculating tax:", error);
                console.error("status:", status);
                console.error("responseText:", xhr.responseText);
                alert('Error calculating tax: ' + xhr.responseText);
            }
        });
    }

    function saveCalculation(calculationData, product_type) {
        const data = {
            "itemName": $("#itemName").val(),
            "price": $("#price").val(),
            "quantity": $("#quantity").val(),
            "state": $("#state").val(),
            "product_type": product_type,
            "tax_paid": calculationData.total_tax
        }
        $.ajax({
            url: "/save_calculation",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function(response) {
                console.log("Calculation saved to database:", response);
                appendHistoryLog(data)
                check_and_update_Piechart({
                    state: data.state,
                    tax_paid: data.tax_paid
                })
            },
            error: function(xhr, status, error) {
                console.error("Error saving calculation:", xhr, status, error);
                alert('Error saving calculation: ' + xhr.responseText);
            }
        });
    }
    function appendHistoryLog(data) {
        const newEntry = `
        <div class="log-entry">
            <div class="top_log">
                <div class="loco">${data.state}</div>
                <div class="price_history">$${data.tax_paid}</div>
            </div>
            <div class="bottom_log">
                <div class="type_name">${data.product_type},</div>
                <div class="product_name">(${data.itemName})</div>
            </div>
        </div>
        `;
        $('.records').prepend(newEntry);
    }
    function check_and_update_Piechart(data){
        $.ajax({
            url: "/top_cost_states",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function(response) {
                console.log("Fetched latest top cost states:", response);
                if (window.myChart) {
                    // Extract states and tax values from response
                    const states = response.map(item => item[0]);
                    const tax = response.map(item => item[1]);
                    const totalPrices = tax.map(amount => (amount + (amount * 0.1)).toFixed(2));
    
                    // Update chart data
                    window.myChart.data = {
                        labels: states,
                        datasets: [{
                            label: 'Tax',
                            data: tax,
                            backgroundColor: [
                                'rgb(117, 117, 159)',
                                'rgb(160, 126, 180)',
                                'rgb(220, 220, 255)'
                            ],
                            hoverOffset: 10
                        }]
                    };
    
                    // Update or recreate the custom text plugin
                    const customTextPlugin = {
                        id: 'customTextPlugin',
                        afterDatasetsDraw(chart) {
                            const ctx = chart.ctx;
                            const dataset = chart.data.datasets[0];
                            const arcs = chart.getDatasetMeta(0).data;
    
                            ctx.save();
                            ctx.font = 'bold 16px inter';
                            ctx.fillStyle = 'white';
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'middle';
    
                            ctx.shadowColor = 'rgba(0, 0, 0, 0.22)';
                            ctx.shadowBlur = 7;
                            ctx.shadowOffsetX = 0;
                            ctx.shadowOffsetY = 1;
    
                            arcs.forEach((arc, index) => {
                                const middleAngle = arc.startAngle + (arc.endAngle - arc.startAngle) / 2;
                                const distanceFromCenter = arc.outerRadius * 0.6;
    
                                const x = arc.x + Math.cos(middleAngle) * distanceFromCenter;
                                const y = arc.y + Math.sin(middleAngle) * distanceFromCenter;
    
                                const text = `${states[index]}: $${totalPrices[index]}`;
                                ctx.fillText(text, x, y);
                            });
    
                            ctx.restore();
                        }
                    };
    
                    // Unregister existing plugin if it exists
                    Chart.unregister(Chart.registry.plugins.get('customTextPlugin'));
                    
                    // Register the updated plugin
                    Chart.register(customTextPlugin);
    
                    // Update chart options if needed
                    window.myChart.options = {
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    };
    
                    // Force a complete redraw
                    window.myChart.update();

                    
                } else {
                    console.warn('Pie chart not found - might not be initialized yet');
                }
            },
            error: function(xhr, status, error) {
                console.error("Error saving calculation:", xhr, status, error);
                alert('Error saving calculation: ' + xhr.responseText);
            }
        });
    }
});
