$(document).ready(function () {
    $("#container").fadeIn()
    setTimeout(()=>{
        $('#productAddContainer').fadeIn()
    },500)
    $('#searchPhoto').click(function () {
      $('#confirmationBox').fadeOut()
        $('#choose').fadeIn()        
        setTimeout(()=>{
          $('#chooseBox').css('display','grid')
          $('#chooseBox').fadeIn()
        }, 500)
    });
    $("#searchPhoto2").click(function () {
      $("#confirmationBox3").fadeOut();
      $("#choose2").fadeIn();
      setTimeout(() => {
        $("#chooseBox2").css("display", "grid");
        $("#chooseBox2").fadeIn();
      }, 500);
    });

    $("#productAddChoice").click(function(){
      $('#container > *').not('#productAddContainer').fadeOut(function(){
        setTimeout(()=>{$("#productAddContainer").fadeIn()},500)
      })
    })
    $('#serviceAddChoice').click(function(){
      $('#container > *').not('#serviceAddContainer').fadeOut(function(){
        setTimeout(()=>{$("#serviceAddContainer").fadeIn()},500)
        
      })
    })
    $('#supplierAddChoice').click(function(){
      $('#container > *').not('#supplierAddContainer').fadeOut(function(){
        setTimeout(()=>{$("#supplierAddContainer").fadeIn()},500)
        
      })
    })


    $('#formButton').click(function(){
      $('#chooseBox').fadeOut()
      $('#choose').fadeIn()
      setTimeout(()=>{
        $("#confirmationBox").css('display','flex')
        $('#confirmationBox').fadeIn()
      }, 500)
    })

    $("#formButton2").click(function () {
      $("#choose1").fadeIn();
      setTimeout(() => {
        $("#confirmationBox2").css("display", "flex");
        $("#confirmationBox2").fadeIn();
      }, 500);
    });

    $("#formButton3").click(function () {
      $("#chooseBox2").fadeOut();
      $("#choose2").fadeIn();
      setTimeout(() => {
        $("#confirmationBox3").css("display", "flex");
        $("#confirmationBox3").fadeIn();
      }, 500);
    });

    apiKey = "H87DWdguLzwxz5jtQcSezyEcpTzf3wKlvZEwBwbm5CsSQ13NUm2yFk3I";
    $('#unsplash').click(function(){
        var query = $('#productName').val()
        console.log(query)
        $.ajax({
          url: "https://api.pexels.com/v1/search",
          method: "GET",
          headers: {
            Authorization: apiKey,
          },
          data: {
            query: query,
            per_page: 1,
          },
          success: function (data) {
            console.log("API Response:", data); // Check API response

            if (data.photos.length > 0) {
                $('#apiIcon').fadeOut();
                $('#apiText').fadeOut();
                var imageUrl = data.photos[0].src.large; // Fetch first image UR
                $("#photoPreview").attr("src", imageUrl); // Set image in <img>
                $("#localPhoto").fadeOut();
                setTimeout(() => {
                  $("#chooseBox").css("gridTemplateColumns", "1fr");
                }, 200);
                setTimeout(() => {
                  $("#photoPreview").fadeIn();
                }, 500);
                let imageUrlText = $("#photoPreview").attr("src");

                if (imageUrlText !== "") {
                  $("#photoUrl").val(imageUrl);
                }
            } else {
              console.log("No images found!");
            }
          },
          error: function (xhr, status, error) {
            console.log(
              "Error fetching image:",
              xhr.responseText || error || "Unknown error"
            );
          },
        });

    })
});