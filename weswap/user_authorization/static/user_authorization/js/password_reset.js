// Function declarations outside DOMContentLoaded
function validateEmail(email) {
    const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return regex.test(email);
}

function button_change(sendOtpBtn, verifyBtn) {
    sendOtpBtn.textContent = 'Resend OTP';
    sendOtpBtn.name = 'resend';
    verifyBtn.style.display = 'block';
    sendOtpBtn.disabled = true;
    setTimeout(() => sendOtpBtn.disabled = false, 10000);
}

function showMessage(messageDiv, message, isError) {
    messageDiv.innerHTML = `<p style="color: ${isError ? 'red' : '#06c843'};">${message}</p>`;
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 3000);
}

document.addEventListener("DOMContentLoaded", function() {
    const forgotPasswordForm = document.getElementById('forgot-password-form');
    const emailInput = document.getElementById('email');
    const emailStatus = document.getElementById('email-status');
    const sendOtpBtn = document.getElementById('send-otp-btn');
    const verifyBtn = document.getElementById('verify-btn');
    const messageDiv = document.getElementById('message');

    // Email validation event listener
    emailInput.addEventListener('input', function() {
        emailStatus.textContent = validateEmail(emailInput.value) ? '✅' : '❌';
        emailStatus.style.color = validateEmail(emailInput.value) ? 'green' : 'red';
    });

    // Form submission event listener
    forgotPasswordForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(forgotPasswordForm);
        const action = event.submitter.name;
        const email = formData.get('email');
        const otp = formData.get('otp');
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        let postData = { email, action: `${action}_otp` };
        if (action === 'verify') postData.otp = otp;

        fetch(forgotPasswordForm.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(postData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                emailInput.classList.add('shake');
                emailInput.value = '';
                emailStatus.textContent = '';
                emailStatus.style.color = '';
                showMessage(messageDiv, data.message, true);
            } else {
                if (data.success) {
                    button_change(sendOtpBtn, verifyBtn);
                    showMessage(messageDiv, data.message, false);
                    if (data.redirect) {
                    // If OTP is verified, redirect to change password page
                    window.location.href = data.redirect;  // Adjust this URL as needed
                }
                } else {
                    showMessage(messageDiv, data.message, true);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage(messageDiv, 'An unexpected error occurred. Please try again.', true);
        });
    });
});