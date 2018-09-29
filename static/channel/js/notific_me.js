$(document).ready(function() {
    var frm = $('#formNotificMe');
    frm.submit(function(event){
        event.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                if(data.notific) {
                    $('#notific').removeClass('active-notific');
                    $('#no-notific').addClass('active-notific');
                }
                else {
                    $('#no-notific').removeClass('active-notific');
                    $('#notific').addClass('active-notific');
                }
            }
        });
        return false;
    });
});