$(document).ready(function(){
    $("#productOrderName").change(function(){
        var productId = $(this).val();

        if (productId) {
            $.ajax({
                url: dynamicDataUrl,
                data: { product_id: productId },
                dataType: "json",
                success: function(response) {
                    $("#productQuantityDynamic").text(response.quantity);
                },
                error: function() {
                    $("#productQuantityDynamic").text("Select A Product");
                }
            });
        } else {
            $("#productQuantityDynamic").text("0");
        }
    });

    $("#productStockName").change(function(){
        var productId = $(this).val();

        if (productId) {
          $.ajax({
            url: dynamicDataUrl,
            data: { product_id: productId },
            dataType: "json",
            success: function (response) {
              $("#productInfo").text(response.quantity);
            },
            error: function () {
              $("#productInfo").text("Select A product");
            },
          });
        } else {
          $("#productInfo").text("0");
        }
    })

    $("#productSaleName").change(function () {
      var productId = $(this).val();

      if (productId) {
        $.ajax({
          url: dynamicDataUrl,
          data: { product_id: productId },
          dataType: "json",
          success: function (response) {
            $("#salesStockQuantity").text(response.quantity);
          },
          error: function () {
            $("#salesStockQuantity").text("Select A product");
          },
        });
      } else {
        $("#salesStockQuantity").text("0");
      }
    });

});