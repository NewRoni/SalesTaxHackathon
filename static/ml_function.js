$(document).ready(function() {
    $("#generateProductType").click(function() {
        var productName = $("#itemName").val();
        $.ajax({
            url: "/text_inference",
            type: "POST",
            data: { product_name: productName },
            success: function(response) {
                console.log(response)
                $("#product_type").val(response);
            },
            error: function(xhr, status, error) {
                console.error("Error generating product type:", error);
                alert('Error generating product type.');
            }
        });
    });

    $("#submitButton").click(function(e) {
        e.preventDefault();
        var formData = $("#taxForm").serialize();
        console.log(formData)
        $.ajax({
            url: "/tax_inference",
            type: "POST",
            data: formData,
            success: function(response) {
                if (response.error) {
                    $("#taxResult").html("Error: " + response.error);
                } else {
                    $("#taxResult").html("Tax Rate: " + response.tax_rate +
                                        "<br>Total Tax: " + response.total_tax +
                                        "<br>Total Price: " + response.total_price);
                }
                success = saveCalculation(response)
                $("#taxForm")[0].reset(); // Clear the form
            },
            error: function(xhr, status, error) {
                console.error("Error calculating tax:", error);
                console.error("status:", status);
                console.error("responseText:", xhr.responseText);
                alert('Error calculating tax: ' + xhr.responseText);
            }
        });
    });
    function saveCalculation(calculationData) {
        const data = {
            "itemName": $("#itemName").val(),
            "price": $("#price").val(),
            "quantity": $("#quantity").val(),
            "state": $("#state").val(),
            "product_type": $("#product_type").val(),
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

