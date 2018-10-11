$('document').ready( function(){
	$('.feedback').on('click',function(){
		var this_ = $(this);
		var op = this_.attr('op');
		$.ajax({
			url: this_.attr('url_'),
			type:'GET',
			beforeSend:function(){
			},
			dataType:'json',
			async:true,
			data:{'opcao':op},
			success:function(json){
				if(json.message != null){
					$("#alert-addPlaylist").html(json.message);
				document.getElementById("alert-addPlaylist").style.visibility = "visible";
				document.getElementById("alert-addPlaylist").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-addPlaylist").style.opacity = "0";
				    document.getElementById("alert-addPlaylist").style.visibility = "hidden";
				}, 1800);
				}
				$("#num-like").html(json.numero_de_likes);
				$("#num-deslike").html(json.numero_de_deslikes);

                if(json.remove_like) {
                    document.getElementById("like").style.backgroundColor = "black";
                }

                if(json.remove_deslike) {
                    document.getElementById("deslike").style.backgroundColor = "black";
                }

                if(json.like) {
                    document.getElementById("like").style.backgroundColor = "#032854";
                }

                if(json.deslike) {
                    document.getElementById("deslike").style.backgroundColor = "#730c0c";
                }
			},
		});
	});
});