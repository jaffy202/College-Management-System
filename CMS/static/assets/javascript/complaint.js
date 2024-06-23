document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("complaint-form");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const registerNumber = document.getElementById("register-number").value;
        const complaintMessage = document.getElementById("complaint-message").value;

        // Send data to Flask route using Fetch API
        fetch('/teacher_index', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                register_number: registerNumber,
                complaint_message: complaintMessage
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data); // Log response from Flask
            // Handle success or failure as needed
        })
        .catch(error => {
            console.error('Error:', error.message);
            // Handle error
        });
        // Clear the form after submission
        form.reset();
    });
});
