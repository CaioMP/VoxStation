$(document).ready(function() {
    var frm = $('#formSavePl');
    frm.submit(function(event){
        event.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                $("#uncheck-playlist").attr("href", "/channel/playlist_all/"+data.playlist_id);
                document.getElementById("uncheck-playlist").style.display = "block";
                document.getElementById("save-playlist").style.display = "none";
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