$(document).ready(function() {
    var frm = $('#reportForm');
    frm.submit(function(event){
        event.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                document.getElementById("motivo").value = "";
                document.getElementById("denuncia").value = "";
                $('#reportAudio').modal('toggle');
                document.getElementById("alert-report").style.visibility = "visible";
				document.getElementById("alert-report").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-report").style.opacity = "0";
				    document.getElementById("alert-report").style.visibility = "hidden";
				}, 1800);
            }
        });
        return false;
    });
});