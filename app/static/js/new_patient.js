document.addEventListener('DOMContentLoaded', function() {


    document.getElementById('patientForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        fetch('/paciente/nuevo_expediente', {
            method: 'POST',
            body: formData
        })
        .then(function(response) {
            return response.json().then(function(data) {
                if (!response.ok) {
                    // Create a custom error object containing the response data
                    let error = new Error(data.message || 'Network response was not ok');
                    error.data = data;
                    throw error;
                }
                return data;
            });
        })
        .then(function(data) {
            // If we reach here, the request was successful (status 2xx)
            setTimeout(function(){
                window.location.href = data.redirect;
            },1000)

        })
        .catch(function(error) {
            // Handle errors if needed
            document.getElementById('response').innerHTML = `<p>An error occurred: ${error.message}</p>`;
            console.error('Error:', error);
            
            // Check if error data includes a redirect URL

        });
    });

});