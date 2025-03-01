$(document).ready(function() {
    $("#submitButton").click(function(e) {
        e.preventDefault();

        var productName = $("#itemName").val();
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
                        const thold = 0.9;
                        console.log("STD RATE: " + std_rate + ", TAX RATE: " + tax_rate);

                        if (std_rate - tax_rate > thold) {
                            $("#taxResult").html("Tax Rate: " + response.tax_rate + "%" +
                                "<br>Total Tax: " + response.total_tax +
                                "<br>Total Price: " + response.total_price +
                                "<br>Note: Tax rates for " + state + " may have tax exemptions or reduced-rate for this product type");
                        } else if (tax_rate - std_rate > thold) {
                            $("#taxResult").html("Tax Rate: " + response.tax_rate + "%" +
                                "<br>Total Tax: " + response.total_tax +
                                "<br>Total Price: " + response.total_price +
                                "<br>Note: Tax rates for " + state + " may have tax-liabilities for this product type");
                        } else {
                            $("#taxResult").html("Tax Rate: " + response.tax_rate + "%" +
                                "<br>Total Tax: " + response.total_tax +
                                "<br>Total Price: " + response.total_price);
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
            "tax_paid": String(calculationData.total_tax)
        }
        $.ajax({
            url: "/save_calculation",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function(response) {
                console.log("Calculation saved to database:", response);
            },
            error: function(xhr, status, error) {
                console.error("Error saving calculation:", xhr, status, error);
                alert('Error saving calculation: ' + xhr.responseText);
            }
        });
    }
});

