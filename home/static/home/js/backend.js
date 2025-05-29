$(document).ready(function () {
  csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;

  function getProduct(element) {
    let productId = $(element).val();
    if (productId != "Add a product") {
      console.log(productId);
      formData = new FormData();
      formData.append("product", productId);
      formData.append("csrfmiddlewaretoken", csrf_token);

      fetch("home/productFetch", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          $(".pqdChild").html(data.product);
          $("productQuantityDynamic").fadeIn();
          // console.log(data.product);
        });
    }
  }
  $("#productOrderName").change(function () {
    getProduct(this);
  });

  $("#productStockName").change(function () {
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
  });

  $("#productSaleName").change(function () {
    getProduct(this);
    // var productId = $(this).val();

    // if (productId) {
    //   $.ajax({
    //     url: dynamicDataUrl,
    //     data: { product_id: productId },
    //     dataType: "json",
    //     success: function (response) {
    //       $("#salesStockQuantity").text(response.quantity);
    //     },
    //     error: function () {
    //       $("#salesStockQuantity").text("Select A product");
    //     },
    //   });
    // } else {
    //   $("#salesStockQuantity").text("0");
    // }
  });

  $("#MachineLearnBtn").click(function () {
    $(".loader").fadeIn()
    let productId = $("#productLearningName").val();
    console.log(productId)
    formData = new FormData();
    formData.append("product", productId);
    formData.append("csrfmiddlewaretoken", csrf_token);

    fetch("home/learn", {
      method: "POST",
      body: formData
    })
      .then((response) => response.json())
      .then((data) => {
        $(".loader").fadeOut()

        $("#machineResponse").html(`
          <span>📦 Product: ${data.product}</span>
          <p>🧮 Next Predicted Sales: ${data.forecast[0].toFixed(2)}</p>
          <p id="AIresponse">🧮 Our systems says : ${data.response}</p>
        `);

      });
  });

  document
    .getElementById("productAddButton")
    .addEventListener("click", function () {
      let formData = new FormData();

      formData.append("productName", $("#productAddName").val());
      formData.append("productDescription", $("#productDescription").html());
      formData.append("productUnits", $("#productUnit").val());
      formData.append("productCategory", $("#productCategory").val());
      formData.append("productCost", $("#productCost").val());
      formData.append("productPrice", $("#productCreationPrice").val());
      formData.append("productStock", $("#productInitialQuantity").val());
      formData.append("csrfmiddlewaretoken", csrf_token);

      fetch("home/addProduct", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Success:", data);
          location.reload();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });

  document.getElementById;
});
