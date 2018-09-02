$(document).ready(function() {
    $('.btn-resp').click(function(event){
        frm_resp = $(this);
        conteudo = frm_resp.parent().parent().find('textarea');

        $.ajax({
            type: frm_resp.parent().parent().attr('method'),
            url: frm_resp.parent().parent().attr('action'),
            data: frm_resp.parent().parent().serialize(),
            success: function (data) {
                if (conteudo.val() != "") {
                    conteudo.val('');
                    $('#alert-comentar').html('Resposta enviada');
                    document.getElementById("alert-comentar").style.visibility = "visible";
                    document.getElementById("alert-comentar").style.opacity = "1";
                    window.setTimeout(function() {
                        document.getElementById("alert-comentar").style.opacity = "0";
                        document.getElementById("alert-comentar").style.visibility = "hidden";
                    }, 1800);
                }
            }
        });
        return false;
    });
});