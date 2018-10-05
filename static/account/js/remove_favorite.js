$(document).ready(function() {
    $(".btn-delFav").click(function(event){
        frm = $(this)
        $.ajax({
            type: frm.parent().attr('method'),
            url: frm.parent().attr('action'),
            data: frm.parent().serialize(),
            success: function (data) {
                $('#alert-remove').html(data.message);
                $('#'+data.audio).remove();
                document.getElementById("alert-remove").style.visibility = "visible";
				document.getElementById("alert-remove").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-remove").style.opacity = "0";
				    document.getElementById("alert-remove").style.visibility = "hidden";
				}, 1800);
				if($("#favoriteslist").children().length == 2){
				    var noFav = document.getElementsByClassName("noFav")[0];
				    noFav.style.display = "block";
				}
            }
        });
        return false;
    });
});