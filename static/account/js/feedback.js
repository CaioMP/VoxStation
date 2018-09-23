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
				console.log(json.message);
				if(json.message != null){
					$("#alert-addPlaylist").html(json.message);
				document.getElementById("alert-addPlaylist").style.visibility = "visible";
				document.getElementById("alert-addPlaylist").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-addPlaylist").style.opacity = "0";
				    document.getElementById("alert-addPlaylist").style.visibility = "hidden";
				}, 1800);
				}
				("#like").text(json.numero_de_likes);
				("#deslike").text(json.numero_de_deslikes);

				
			},
			error:function(){
				alert("erro ao conectar com servidor");
			}
		});
	});
});