document.getElementById("otpForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent default form submission

    let otp = document.getElementById("otp").value;
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("{% url 'verify_otp' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken  // Include CSRF token in headers
        },
        body: JSON.stringify({ otp: otp })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_url;  // Redirect on success
        } else {
            document.getElementById("otp-error").textContent = data.message;
            document.getElementById("otp-error").style.display = "block";
        }
    })
    .catch(error => console.error("Error:", error));
});