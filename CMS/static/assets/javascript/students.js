document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var form = document.getElementById('uploadForm');
    var formData = new FormData(form);

    fetch('/add_students', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerText = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});