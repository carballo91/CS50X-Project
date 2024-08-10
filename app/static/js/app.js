$(document).ready(function() {

    function fadeMessage(messageClass){
        setTimeout(() => {
            $(messageClass).fadeOut('slow');
        }, 5000); 
    }
    fadeMessage('.alert')
    fadeMessage('.success')
    fadeMessage('.warning')

    $('#patientNotificationsButton').click(function(){
        $('#patientNotifications').slideDown();
    })

    $('#prescriptionNotificationsButton').click(function(){
        $('#prescriptionNotifications').slideDown();
    })

});