function toggleFields() {
    var userType = document.querySelector('input[name="user_type"]:checked').value;

    // Hide all fields first
    document.querySelectorAll('.student-fields, .parent-fields, .teacher-fields, .hod-fields, .admin-fields').forEach(function(field) {
        field.style.display = 'none';
    });

    // Remove 'required' attribute from all input fields
    document.querySelectorAll('.inputbox input').forEach(function(input) {
        input.removeAttribute('required');
    });

    // Show fields based on selected user type
    if (userType === 'student') {
        document.querySelector('.student-fields').style.display = 'block';
        document.querySelectorAll('.student-fields input').forEach(function(input) {
            input.setAttribute('required', 'required');
        });
        document.getElementById('registerContainer').style.display = 'flex';
        document.getElementById('registerLink').href = registrationUrls['register'];
        document.getElementById('forget_password').href = registrationUrls['stu_forget'];
        document.getElementById('forget_password').style.display = 'block';
    } else if (userType === 'parent') {
        document.querySelector('.parent-fields').style.display = 'block';
        document.querySelectorAll('.parent-fields input').forEach(function(input) {
            input.setAttribute('required', 'required');
        });
        document.getElementById('registerContainer').style.display = 'flex';
        document.getElementById('registerLink').href = registrationUrls['parent_register'];
        document.getElementById('forget_password').href = registrationUrls['par_forget'];
        document.getElementById('forget_password').style.display = 'block';
    } else if (userType === 'teacher') {
        document.querySelector('.teacher-fields').style.display = 'block';
        document.querySelectorAll('.teacher-fields input').forEach(function(input) {
            input.setAttribute('required', 'required');
        });
        document.getElementById('registerContainer').style.display = 'flex';
        document.getElementById('registerLink').href = registrationUrls['teacher_register'];
        document.getElementById('forget_password').href = registrationUrls['tec_forget'];
        document.getElementById('forget_password').style.display = 'block';
    } else if (userType === 'hod') {
        document.querySelector('.hod-fields').style.display = 'block';
        document.getElementById('registerContainer').style.display = 'none';
        document.getElementById('forget_password').style.display = 'none';
    } else if (userType === 'admin') {
        document.querySelector('.admin-fields').style.display = 'block';
        document.getElementById('registerContainer').style.display = 'none';
        document.getElementById('forget_password').href = registrationUrls['ad_forget'];
        document.getElementById('forget_password').style.display = 'block';
    }
}

// Add event listener to radio buttons
var radioButtons = document.querySelectorAll('input[name="user_type"]');
radioButtons.forEach(function(radioButton) {
    radioButton.addEventListener('change', toggleFields);
});

// Initially show fields based on default selection
toggleFields();
// // Function to show/hide fields based on selected user type
// function toggleFields() {
//     var userType = document.querySelector('input[name="user_type"]:checked').value;

//     // Hide all fields first
//     document.querySelectorAll('.student-fields, .parent-fields, .teacher-fields, .hod-fields, .admin-fields').forEach(function(field) {
//         field.style.display = 'none';
//     });

//     // Show fields based on selected user type
//     if (userType === 'student') {
//         document.querySelector('.student-fields').style.display = 'block';
//         document.getElementById('registerContainer').style.display = 'flex';
//         document.getElementById('registerLink').href = registrationUrls['register'];
//     } else if (userType === 'parent') {
//         document.querySelector('.parent-fields').style.display = 'block';
//         document.getElementById('registerContainer').style.display = 'flex';
//         document.getElementById('registerLink').href = registrationUrls['parent_register'];
//     } else if (userType === 'teacher') {
//         document.querySelector('.teacher-fields').style.display = 'block';
//         document.getElementById('registerContainer').style.display = 'flex';
//         document.getElementById('registerLink').href = registrationUrls['teacher_register'];
//     } else if (userType === 'hod') {
//         document.querySelector('.hod-fields').style.display = 'block';
//         document.getElementById('registerContainer').style.display = 'none';
//     } else if (userType === 'admin') {
//         document.querySelector('.admin-fields').style.display = 'block';
//         document.getElementById('registerContainer').style.display = 'none';
//     }
// }

// // Add event listener to radio buttons
// var radioButtons = document.querySelectorAll('input[name="user_type"]');
// radioButtons.forEach(function(radioButton) {
//     radioButton.addEventListener('change', toggleFields);
// });

// // Initially show fields based on default selection
// toggleFields();
