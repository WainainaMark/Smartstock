document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll(".linkText");
  const chartIcon = document.getElementById("chartIcon");
  const pieChartIcon = document.getElementById("pieChartIcon");
  const homeIcon = document.getElementById("homeIcon");
  const loader = document.getElementById('loader')

  links.forEach((link, index) => {
    link.addEventListener("click", () => {
      
      if (index === 0) {
        homeIcon.classList.add("showHome");
        link.prepend(loader);
        setTimeout(() => window.location.href = "{% url 'home' %}", 600);

      } else if (index === 1) {
        chartIcon.classList.add("analyse");
        link.appendChild(loader)
        
      } else if (index === 2) {
        pieChartIcon.style.transform = `rotate(${Math.floor(
          Math.random() * 360
        )}deg)`;
        link.appendChild(loader)
      }
      loader.style.display = 'block'
    });
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
