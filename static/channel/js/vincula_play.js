$('document').ready( function(){
	$('#salvarVinculo').on('click',function(){
		console.log('disparo funciona')
		var this_ = $(".dm-vincular");
		var valor = $("input[name=canal]:checked").val();
		$.ajax({
			url: this_.attr('url_'),
			type:'GET',
			beforeSend:function(){
				
			},
			dataType:'json',
			async:true,
			data:{'playlist':this_.attr('id_'),'canal':valor},
			success:function(json){
				console.log(json);
				$("#alert-addPlaylist").html(json.message);
				document.getElementById("alert-addPlaylist").style.visibility = "visible";
				document.getElementById("alert-addPlaylist").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-addPlaylist").style.opacity = "0";
				    document.getElementById("alert-addPlaylist").style.visibility = "hidden";
				}, 1800);
				$('#play_load').html(json.html);
			},
			error:function(){
				alert("fudeu bahia");
			}
		});
	});
});