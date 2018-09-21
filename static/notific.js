$(document).ready(function() {
    var frm = $('#formNotific');
    frm.submit(function(event){
        event.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
        });
        return false;
    });
});