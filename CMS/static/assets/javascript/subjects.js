
    $(document).ready(function () {
        $('#branch').change(function () {
            var selectedBranch = $(this).val();
            if (selectedBranch !== "") {
                // Make AJAX request to Flask function to get subjects based on branch
                $.ajax({
                    url: '/get_subjects',
                    type: 'POST',
                    data: {branch: selectedBranch},
                    success: function (response) {
                        $('#subject').empty();
                        $.each(response.subjects, function(index, subject) {
                            $('#subject').append($('<option>', {
                                value: subject,
                                text: subject
                            }));
                        });
                        $('#subject').prop('disabled', false);
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            } else {
                $('#subject').empty().append('<option value="" selected disabled>Choose Branch First</option>');
                $('#subject').prop('disabled', true);
            }
        });
    });
