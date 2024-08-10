$(document).ready(function() {
    $('#findPatientForm').on('submit', function(event) {
      event.preventDefault()
      $.ajax({
        type: 'get',
        url: find_patient_url,
        data: $(this).serialize(),
        success: function(response) {
          id = response.id
          $('#message').empty();
          $('#patient').empty();
          $('#send').empty();
          if (response.found) {
            $('#patient').append(
                '<tr><td>' + response.name + '</td>' + 
                '<td>' + response.last_name + '</td>' +
                '<td>' + response.age + '</td>' + 
                '<td>' + response.address + '</td></tr>'
            );
            //$('#send').append(response.send_form);
            $('#send').html(`<form id="searchForm" action="${response.url}" method="post">
              ${response.send_form}
              </form>`)
            $('#searchForm').on('submit', function(event){

              event.preventDefault();
              // Extract other form data if needed
              $.ajax({
                  type : 'POST',
                  url: '/paciente/enviar_notificacion_consulta/' + encodeURIComponent(parseInt(id)),
                  data : $(this).serialize(),
                  success: function(secondResponse) {
                      // This is the success callback of the nested AJAX request
                      $('#message').append('<p>Notificacion de Consulta Enviada</p>')
                      $('#patient').empty();
                      $('#send').empty();
                  },
                  error: function(xhr2, status2, error2) {
                      // Handle errors for the nested AJAX request
                      console.error('Error in second AJAX request:', error2);
                  }
              })
            })
          } else {
              $('#patient').append('<p>No existe registro.</p>');
              $('#send').html(`<form id="newFile" action="${response.url}" method="post">
                ${response.send_form}
                </form>`)
          }

        },
        error: function() {
          $('#patient').empty()
          $('#patient').append('Ocurrio un error.');
        }
      });
    });
  });