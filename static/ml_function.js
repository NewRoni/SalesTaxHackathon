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
});
