$(document).ready(function() {
    var frm = $('#searchAudiosForm');
    frm.submit(function(event){
        event.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                var col = document.getElementsByClassName("col-audios");
                var no_search = document.getElementById("no-search");

                for(i = 0; i < col.length; i++) {
                    col[i].style.display = "none";
                }

                if (data.audios.length) {
                    no_search.style.visibility = "hidden";
                    no_search.style.opacity = "0";

                    for(i = 0; i < data.n_audios; i++) {
                        col = document.getElementsByClassName("col-audios")[i];

                        for(x = 0; x < data.audios.length; x++)
                            if(col.id == data.audios[x]) {
                                col.style.display = "block";
                            }
                    }
                }
                else {
                    no_search.style.visibility = "visible";
                    no_search.style.opacity = "1";
                }
            }
        });
        return false;
    });
});