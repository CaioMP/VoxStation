$(document).ready(function() {
    var frm = $('#comentarForm');
    frm.submit(function(event){
        event.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                document.getElementById("id_conteudo").value = "";
                $('#alert-comentar').html('Comentário enviado');
                document.getElementById("alert-comentar").style.visibility = "visible";
				document.getElementById("alert-comentar").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-comentar").style.opacity = "0";
				    document.getElementById("alert-comentar").style.visibility = "hidden";
				}, 1800);
            }
        });
        return false;
    });
});