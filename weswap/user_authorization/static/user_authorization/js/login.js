document.addEventListener("DOMContentLoaded", function() {
    // Check for error and add shake effect
    const loginForm = document.getElementById('loginForm');
    if (loginForm && loginForm.dataset.error === 'true') {
        const passwordField = document.getElementById('password');
        if (passwordField) {
            passwordField.classList.add('shake');
            passwordField.value = '';
        }
    }

    // Handle messages
    var messages = document.querySelector('.messages');
    if (messages) {
        // Remove messages after 3 seconds
        setTimeout(function() {
            messages.style.transition = "opacity 0.5s ease";
            messages.style.opacity = 0;
            setTimeout(function() {
                messages.remove();
            }, 500);
        }, 3000);
    }
});