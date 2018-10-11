$('document').ready( function(){
	$('#add_redes_sociais').on('click',function(){
		var this_ = $(this);
		var redes = {
			'twitch':$('#twitch').val(),
			'facebook':$('#facebook').val(),
			'youtube':$('#youtube').val(),
			'googleplus':$('#googleplus').val(),
			'twitter':$('#twitter').val(),
			'instagram':$('#instagram').val(),
		};
		$.ajax({
			url:this_.attr('uc'),
			type:'GET',
			dataType:'json',
			data:redes,
			success:function(json){
				$("#alert-addPlaylist").html(json.message);
				document.getElementById("alert-addPlaylist").style.visibility = "visible";
				document.getElementById("alert-addPlaylist").style.opacity = "1";
				window.setTimeout(function(){
				    document.getElementById("alert-addPlaylist").style.opacity = "0";
				    document.getElementById("alert-addPlaylist").style.visibility = "hidden";
				}, 5000);
			},
		});
	});
});