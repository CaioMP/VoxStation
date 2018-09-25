$(document).ready(function() {
    $('.delete').click(function(event){
        btn = $(this);
        form = $("form");
        frm_del = btn.parent().find(form);

        $.ajax({
            type: frm_del.attr('method'),
            url: frm_del.attr('action'),
            data: frm_del.serialize(),
            success: function (data) {
                btn.parent().remove();
                audios = document.getElementsByClassName("audio");
                for(var i = 0; i < audios.length; i++){
                    var audio = "#" + audios[i].id;
                    var num_audio = $(audio).find('.numero-audio');
                    num_audio.html(i+1);
                }
                $('#num-audios').html(data.num_audios);
                $('#last-update').html(data.dia + " de " + data.mes + " de " + data.ano + " às " + data.horario);

                $('#alert-comentar').html(data.message);
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