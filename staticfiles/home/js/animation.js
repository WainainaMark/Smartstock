$("document").ready(function(){
    $("#productAddCloseIcon").click(function () { 

        
        $("#productAddForm").css("transform", "translateY(-20px)");
        setTimeout(() => {
            $("#productAddForm").css("transform", "translateY(120%)");
        }, 300);
        setTimeout(() => {
            $("#productAddContainer").fadeOut()
            
        }, 600);
    });

    $(".addProductToggle").click(()=>{
        $("#productAddForm").css("transition", "transform 0.5s ease-in-out");
        $("#productAddForm").css("transform", "translateY(120%)")
        setTimeout(() => {
            $("#productAddForm").css("transform", "translateY(0)");
        }, 600);
    })

    $("#feedBackButton").click(function(){
        $("#feedbackContainer").fadeOut()
    })

    

    $('.reportBox').click(function(){
        $('.boxTitle').css("fontSize", "1.125rem")
        $('.dynamicData').css("opacity", "0")
        $(".reportText").css({
            "transform": "translate(-50%,-50%)",
            "left": "50%"
        })
        $('.analytic').css({
            "opacity": "0",
            "transform": "translateY(10px)"
        })

        $(this).find('.boxTitle').css("fontSize", "2rem")
        $(this).find('.reportText').css({
            "transform": "translate(0px,0px)",
            "left": "10px"
        })
        $(this).find('#salesAmount').css("left", "0px")
        $(this).find('#clock').css("left", "0px")
        $(this).find('.dynamicData').css("opacity", "1")

        setTimeout(()=> {
            $(this).find(".dynamicData").css("transform", "translateY(-50%)"),
            $(this).find(".analytic").css({
                "opacity": "1",
                "transform": "translateY(0px)"
            })
            
        }, 150 )
        
    })

    $('#features').click(function(){
        $('.boxTitle').css("fontSize", "1.125rem")
        $('.dynamicData').css("opacity", "0")
        $(".reportText").css({
            "transform": "translate(-50%,-50%)",
            "left": "50%"
        })
        
    })

    
})