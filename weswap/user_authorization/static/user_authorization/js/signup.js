document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signup-form');
    const sendOtpBtn = document.getElementById('send-btn');
    const signupBtn = document.getElementById('signup-btn');
    const emailInput = document.getElementById('email');
    const emailLabel = document.getElementById('email-label');
    let email;

    // Disable signup button initially
    signupBtn.disabled = true;

    // Function to read all form variables
    function getFormData() {
        console.log(email)
        return {
            username: document.getElementById('username').value,
            email: email,
            password: document.getElementById('password').value,
            gender: document.getElementById('gender').value,
            department: document.getElementById('dept').value,
            current_year: document.getElementById('year').value
        };
    }

    // Event listener for send OTP button
    sendOtpBtn.addEventListener('click', function(e) {
        e.preventDefault();
        email = emailInput.value;

        // AJAX request to send OTP
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ email: email, action: 'send-otp'})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Change button to verify OTP
                sendOtpBtn.textContent = 'Verify';
                sendOtpBtn.id = 'verify-otp-btn';
                // Change email input and label
                emailInput.id = 'otp';
                emailInput.name = 'otp';
                emailInput.value = '';
                emailInput.type = 'text';
                emailLabel.textContent = 'Enter OTP:';

                sendOtpBtn.disabled = false;

                // Add event listener for OTP verification
                sendOtpBtn.removeEventListener('click', arguments.callee);
                sendOtpBtn.addEventListener('click', verifyOtp);
                alert(data.message);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });

    // Function to verify OTP
    function verifyOtp(e) {
        e.preventDefault();
        const enteredOtp = document.getElementById('otp').value;
        console.log(enteredOtp)

        // AJAX request to verify OTP (if needed for server-side verification)
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ otp: enteredOtp, action: 'verify-otp'})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                document.getElementById('verify-otp-btn').disabled = true;
                signupBtn.disabled = false;
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }

// Function to check if all required fields are filled
function validateForm(formData) {
    const requiredFields = ['username', 'email', 'password', 'gender', 'department', 'current_year'];
    const emptyFields = [];

    for (const field of requiredFields) {
        if (!formData[field]) {
            emptyFields.push(field);
        }
    }

    return emptyFields;
}

// Event listener for signup button
signupBtn.addEventListener('click', function(e) {
    e.preventDefault();
    const formData = getFormData();
    const emptyFields = validateForm(formData);

    if (emptyFields.length > 0) {
        alert(`Please fill in the following fields: ${emptyFields.join(', ')}`);
        return;
    }

    console.log('Form data:', formData);

    // Send the data to your server
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ ...formData, action: 'signup' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Signup successful!');
            // Optionally redirect the user or clear the form
            window.location.href = data.redirect;
        } else {
            alert(`Signup failed: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during signup. Please try again.');
    });
});
});