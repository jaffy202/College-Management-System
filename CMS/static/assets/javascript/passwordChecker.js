function checkPasswords() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
        alert("Password and confirm password do not match!");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}
