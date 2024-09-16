const savebtn = document.getElementById('change-pass-btn');
const new_pass = document.getElementById('new_password');
const verify_pass = document.getElementById('confirm_password');
const change_form = document.getElementById('change-password-form');
const messageDiv = document.getElementById('message');
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function showMessage(messageDiv, message, isError) {
    messageDiv.innerHTML = `<p style="color: ${isError ? 'red' : '#06c843'};">${message}</p>`;
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 5000);
}

savebtn.addEventListener('click', function(e) {
    e.preventDefault(); // Prevent form from submitting normally
    console.log(new_pass)
    console.log(verify_pass)
    // Check if passwords match
    if (new_pass.value !== verify_pass.value) {
        showMessage(messageDiv, "Passwords do not match. Please try again.", true);
        return;
    }

    // If passwords match, proceed with AJAX request
    fetch(change_form.action, {
        method: 'POST',
        body: JSON.stringify({
            new_password: new_pass.value,
            verify_password: verify_pass.value
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(messageDiv, data.message, false);
            window.location.href = data.redirect; // Redirect to login page
        } else {
            showMessage(messageDiv, data.message, true);
            new_pass.textContent = '';
            verify_pass.textContent = '';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage(messageDiv, "An error occurred. Please try again.");
    });
});