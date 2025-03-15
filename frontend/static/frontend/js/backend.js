$(document).ready(function () {
  $("#productUnit").change(function () {
    var productUnit = $(this).val();
    $("#productCostUnitText").html("For each " + productUnit);
    $("#productPriceUnitText").html("For each " + productUnit);
  });


  $("#fileInput").change(function (event) {
    let file = event.target.files[0];

    if (file) {
      let reader = new FileReader();

      reader.onload = function (e) {
        $("#apiIcon2").fadeOut()
        $("#localPhotoText").fadeOut()

        let img = $("#localPhotoPreview").attr("src", e.target.result)
        $('#unsplash').fadeOut()
        setTimeout(()=>{
            $("#chooseBox").css("gridTemplateColumns", "1fr");
        },200)
        setTimeout(()=>{
            $('#localPhotoPreview').fadeIn()
        }, 500)

        $("#localPhoto").append(img);
      };

      reader.readAsDataURL(file);
    }
  });

  $("#saveImage").click(function(event){
    event.preventDefault()
    let imageUrl = $("#photoPreview").attr("src");

    $.ajax({
      url: "/frontend/downloadImage", // Django view URL
      type: "GET",
      data: { image_url: imageUrl }, // GET request (No POST needed)
      success: function (response) {
        alert(response.message); // Show success message
      },
      error: function () {
        alert("Failed to download image.");
      },
    });
  })

  $("#formButton").click(function () {
      let description = $("#productDescriptionInput").html();
      console.log(description) // Get content
      $("#descriptionInput").val(description)
      

      // $('#productAddButton').click(function(){
        // fetch("", {
        //   method: "POST",
        //   headers: {
        //     "Content-Type": "application/json",
        //     "X-CSRFToken": getCookie("csrftoken"), // CSRF protection
        //   },
        //   body: JSON.stringify({ description: description }),
        //   contentType: 'application/json'
        // })
        //   .then((response) => response.json())
        //   .then((data) => console.log(data))
        //   .catch((error) => console.error("Error:", error));
      // })

    });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
