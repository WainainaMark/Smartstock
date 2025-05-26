document.addEventListener("DOMContentLoaded", function () {
    function checkInputs(){
        let productCost = document.getElementById('productCost').value
        let productPrice = document.getElementById('productPrice').value
        const defaultText = document.getElementById('defaultText')
        const netResultHTML = document.getElementById('netResult')
        const netResultHTMLInfo = document.getElementById("netResultInfo");
        const financialHeading = document.getElementById('financialHeading')
        const profitIcon = document.getElementById('profitIcon')
        const lossIcon = document.getElementById("lossIcon");

        if (isNaN(productCost) || isNaN(productPrice)) {
            profitIcon.classList.remove('show')
            lossIcon.classList.remove('show')
            netResultHTML.style.color = "black"
            netResultHTML.innerHTML = "";
            netResultHTMLInfo.innerHTML= ""
            netResultHTML.innerHTML = "Enter a valid number";

            return;
        }

        if(productCost && productPrice){
            financialHeading.style.display = "block"
            profitIcon.style.display = "flex"
            lossIcon.style.display = "flex";
            defaultText.style.opacity = "0"
            setTimeout(()=>{
                defaultText.style.display = "none"
                financialHeading.style.opacity = "1"
            }, 500)
            setTimeout(()=>{
                net = productPrice-productCost
                net = net.toLocaleString()
                netResult = ((productPrice - productCost) / productPrice) * 100;
                if(netResult>0){
                    netResultHTML.style.color = 'green'
                    profitIcon.classList.add('show')
                }
                else{
                    netResultHTML.style.color = "red"
                    profitIcon.classList.remove("show");
                    lossIcon.classList.add('show')
                }
                netResult = netResult.toFixed(2)
                netResultHTML.innerHTML = netResult + "%"
                netResultHTMLInfo.innerHTML = net + "Ksh per sale. "
            }, 500)

            
        }

        
    }

    document.getElementById('productCost').addEventListener('input', checkInputs)
    document.getElementById('productPrice').addEventListener('input', checkInputs)
    counter = 0
    if(counter==0){
        document
          .querySelector("#localPhoto")
          .addEventListener("click", function () {
            document.getElementById("fileInput").click();
          });
          counter = counter + 1
    }
    else{
        return 0;
    }
})