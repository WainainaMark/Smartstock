document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll(".linkText");
  const chartIcon = document.getElementById("chartIcon");
  const pieChartIcon = document.getElementById("pieChartIcon");
  const homeIcon = document.getElementById("homeIcon");
  const loader = document.getElementById("loader");

  links.forEach((link, index) => {
    link.addEventListener("click", () => {
      if (index === 0) {
        homeIcon.classList.add("showHome");
        link.prepend(loader);
      } else if (index === 1) {
        chartIcon.classList.add("analyse");
        link.appendChild(loader);
      } else if (index === 2) {
        pieChartIcon.style.transform = `rotate(${Math.floor(
          Math.random() * 360
        )}deg)`;
        link.appendChild(loader);
      }
      loader.style.display = "block";
    });
  });


function updateClock() {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, "0");
  const minutes = now.getMinutes().toString().padStart(2, "0");
  const timeString = `${hours}:${minutes}`;
  document.getElementById("clock").textContent = timeString;
}

setInterval(updateClock, 30000); // Update every second
updateClock();

const buttons = document.querySelectorAll(".button");
const order = document.getElementById("orderBox");
const sales = document.getElementById("salesBox");
const parentBox = document.getElementById("userActions");
const childBox = document.querySelectorAll("userActionBoxes");
const closeIcon = document.querySelectorAll(".closeIcon");
const closeIconSvg = document.getElementById("closeIcon");
const closeIconSvg2 = document.getElementById("closeIcon2");
const salesForm = document.getElementById("salesForm");
const stockForm = document.getElementById("stockForm");
const orderFormBtn = document.getElementById("#orderButton");
const choices = document.querySelectorAll(".userChoices");
const activeChoice = document.getElementById("activeChoice");
const activeChoiceParent = document.getElementById("userActionChoice");
const choice1 = document.getElementById("choice1");
const choice2 = document.getElementById("choice2");
const formContainer = document.getElementById("formContainer");
const productCloseIcon = document.getElementById("closeIcon2a");
const productAddContainer = document.getElementById("productAddContainer");
const productAddForm = document.getElementById("productAddForm");
const productAddToggles = document.querySelectorAll(".addProductToggle");
const actionBoxTitles = document.querySelectorAll(".actionBoxTitle");
const displayTitle = document.getElementById("displayTitle");
const orderDisplayTitle = document.getElementById("displayTitle1");
const informativeTitle = document.getElementById("informativeTitle");
const orderinformativeTitle = document.getElementById("informativeTitle1");
const productOrder =document.getElementById('productOrderName')
productCloseIcon.addEventListener("click", () => {
  setTimeout(() => (productAddContainer.style.display = "none"), 1000);
});

productOrder.addEventListener('click', () => {
  const value = productOrder.value;
  if(value == 'Add a product'){
    productAddContainer.style.display = 'flex'
    productAddContainer.style.opacity = 1
    $("#productAddForm").css("transition", "transform 0.5s ease-in-out");
        $("#productAddForm").css("transform", "translateY(120%)")
        setTimeout(() => {
            $("#productAddForm").css("transform", "translateY(0)");
        }, 600);
  }
});

choices.forEach((choice, index) => {
  choice.addEventListener("click", () => {
    if (index == 0) {
      activeChoice.style.left = "23%";
      activeChoice.style.width = "46%";
      choice.style.color = "white";
      choice2.style.color = "black";
      formContainer.style.transform = "translateX(0)";
      formContainer.classList.remove("translate");
    } else if (index == 1) {
      activeChoice.style.left = "73%";
      activeChoice.style.width = "54%";
      choice.style.color = "white";
      choice1.style.color = "black";
      formContainer.style.transform = "translateX(-50%)";
      formContainer.classList.add("translate");
    }
  });
});

buttons.forEach((button, index) => {
  button.addEventListener("click", () => {
    closeIcon.forEach((close) => {
      setTimeout(() => close.classList.add("appear"), 500);
    });
    displayTitle.style.opacity = "0";
    orderDisplayTitle.style.opacity = "0";
    setTimeout(() => {
      (displayTitle.style.display = "none"),
        (orderDisplayTitle.style.display = "none");
    }, 500);

    parentBox.style.gap = "0px";

    if (index == 0) {
      sales.classList.add("null");
      button.style.opacity = "0";
      orderinformativeTitle.style.display = "flex";
      setTimeout(() => {
        closeIconSvg.classList.add("rotateIcon");
        formContainer.style.display = "flex";
        activeChoiceParent.style.display = "flex";
        button.style.display = "none";
        orderinformativeTitle.style.opacity = "1";
      }, 600);
    } else if (index == 1) {
      order.classList.add("null");
      button.style.opacity = "0";
      informativeTitle.style.display = "flex";

      setTimeout(() => {
        (informativeTitle.style.opacity = "1"),
          closeIconSvg2.classList.add("rotateIcon");
        salesForm.style.display = "flex";
        button.style.display = "none";
      }, 600);
    }
  });
});

closeIcon.forEach((close) => {
  close.addEventListener("click", () => {
    closeIcon.forEach((close) => {
      close.classList.remove("appear");
      closeIconSvg.classList.remove("rotateIcon");
      closeIconSvg2.classList.remove("rotateIcon");
    });
    buttons.forEach((button) => {
      button.style.opacity = "1";
    });
    displayTitle.style.display = "flex";
    orderDisplayTitle.style.display = "flex";
    informativeTitle.style.display = "none";
    orderinformativeTitle.style.display = "none";
    setTimeout(() => {
      (displayTitle.style.opacity = "1"),
        (orderDisplayTitle.style.opacity = "1");
      informativeTitle.style.opacity = "0";
      orderinformativeTitle.style.opacity = "0";
    }, 500);
    parentBox.style.gap = "20px";
    order.classList.remove("null");
    sales.classList.remove("null");
    setTimeout(() => {
      formContainer.style.display = "none";
      salesForm.style.display = "none";
      activeChoiceParent.style.display = "none";
      buttons.forEach((button) => {
        button.style.display = "block";
      });
    }, 135);
  });
});

document.addEventListener(
  "wheel",
  function (event) {
    if (event.ctrlKey) {
      event.preventDefault();
    }
  },
  { passive: false }
);

document.addEventListener(
  "gesturestart",
  function (event) {
    event.preventDefault();
  },
  { passive: false }
);

document.addEventListener(
  "gesturechange",
  function (event) {
    event.preventDefault();
  },
  { passive: false }
);

document.addEventListener(
  "gestureend",
  function (event) {
    event.preventDefault();
  },
  { passive: false }
);

const motherContainer = document.getElementById("homeContent");
const reportContainer = document.getElementById("report");
const featuresContainer = document.getElementById("features");
const reportBoxes = document.querySelectorAll(".reportBox");
const homeContainer = document.getElementById("features");
const days = Array.from(document.querySelectorAll('.day'))
// const date = new Date()
// const dayNumber = date.getDay() - 1
// console.log(dayNumber)

// days[dayNumber].style.backgroundColor = "#34352c"
// days[dayNumber+7].style.backgroundColor = "#34352c"
// days[dayNumber+14].style.backgroundColor = "#34352c"
// days[dayNumber+21].style.backgroundColor = "#34352c"



reportBoxes.forEach((reportBox, index) => {
  counter = 1;
  reportBox.addEventListener("click", () => {
    console.log(counter);
    
    reportBoxes.forEach((reportBox) => {
      reportBox.classList.remove("full");
    });
    reportBox.classList.add("full");
    
    counter = counter + 1;
    console.log(counter);
    setTimeout(() => {
      reportContainer.classList.add("phoneResize");
    }, 500);
    motherContainer.classList.add("initPhoneResize");

    if (index == 0) {
      console.log("Total Sales");

    } else if (index == 1) {
      console.log("Total Orders");
    } else if (index == 2) {
      console.log("Total Stock");
    } else if (index == 3) {
      console.log("Total Profit");
    }
    console.log(counter);
  });
});

homeContainer.addEventListener("click", () => {
  reportBoxes.forEach((reportBox) => {
    reportBox.classList.remove("full");
  });
});

})
