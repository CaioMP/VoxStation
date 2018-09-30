$(document).ready(function() {
    var frm = $('#searchPlaylistForm');
    frm.submit(function(event){
        event.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                var col = document.getElementsByClassName("col-playlist");
                var no_search = document.getElementById("no-search-pl");

                for(i = 0; i < col.length; i++) {
                    col[i].style.display = "none";
                }

                if (data.playlists.length) {
                    no_search.style.visibility = "hidden";
                    no_search.style.opacity = "0";

                    for(i = 0; i < data.n_playlists; i++) {
                        col = document.getElementsByClassName("col-playlist")[i];

                        for(x = 0; x < data.playlists.length; x++)
                            if(col.id == data.playlists[x]) {
                                col.style.display = "inline-flex";
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