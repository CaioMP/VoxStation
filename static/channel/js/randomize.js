$(document).ready(function() {
    var frm = $('#randomizeForm');
    frm.submit(function(event){
        event.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            dataType:'json',
            async:true,
            success: function (data) {
                $("#proximo").attr("href", "/channel/playlist_play/" + data.playlist + "/" + data.proximo)
            }
        });
        return false;
    });
});