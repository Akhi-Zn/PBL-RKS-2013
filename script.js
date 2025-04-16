document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("check-btn").addEventListener("click", async function () {
        const email = document.getElementById("email").value;

        if (!validateEmail(email)) {
            alert("Please enter a valid email address.");
            return;
        }

        const isValid = await checkEmailExists(email);
        if (isValid) {
            sendEmail(email);
        } else {
            alert("This email is not registered or does not exist.");
        }
    });
});

// Fungsi validasi format email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Fungsi untuk memeriksa apakah email valid dan terdaftar
async function checkEmailExists(email) {
    const API_KEY = "1e4433bd7bf944228d6237e67908ce1a"; // Ganti dengan API Key dari Abstract API
    const url = `https://emailvalidation.abstractapi.com/v1/?api_key=${API_KEY}&email=${email}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        return data.deliverability === "DELIVERABLE";
    } catch (error) {
        console.error("Error checking email:", error);
        return false;
    }
}

// Fungsi untuk mengirim email dengan EmailJS
function sendEmail(email) {
    emailjs.init("GLNrJHX_8Smab9XOB"); // Ganti dengan EmailJS Public Key
    console.log("EmailJS initialized successfully.");

    const templateParams = {
        To_Email: email,
    };

    console.log("Sending email with params:", templateParams);

    emailjs.send("service_is0ydup", "template_xxi1rc5", templateParams)
        .then(response => {
            console.log("Email sent successfully!", response);
            alert("Email has been sent successfully!");
        })
        .catch(error => {
            console.error("Failed to send email:", error);
            alert("Failed to send email.");
        });
    
    document.getElementById("result-message").classList.remove("hidden");
    document.getElementById("result-message").innerText = `✅ An email has been sent to ${email} with further instructions.`;        
}
