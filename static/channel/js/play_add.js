$('document').ready( function(){
	$('.addplay').on('click',function(){
		var this_aud = $(this);
		var audio = this_aud.attr('aud_atre');
		$.ajax({
				url: this_aud.attr('url_'),
				type:'GET',
				beforeSend:function(){
					
				},
				data:{'aud':audio,'new':false, 'load':true},
				dataType:'json',
				async:true,
				success:function(json){
					$('#play_load').html(json.html);
					$('.play_id').attr('aud',audio);
					$('#form_playlist').attr('aud',audio)
				},
			});
	});
	$('body').on('click','.play_id',function(){
		var this_play = $(this);
		var playlist = this_play.attr('id');
		var aud = this_play.attr('aud');
		$.ajax({
			url: '/channel/playlist_add_audio',
			type:'GET',
			beforeSend:function(){
						
			},
			data:{'playlist_cod':playlist,'aud':aud},
			dataType:'json',
			async:true,
			success:function(json){
				$("#alert-addPlaylist").html(json.message);
				document.getElementById("alert-addPlaylist").style.visibility = "visible";
				document.getElementById("alert-addPlaylist").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-addPlaylist").style.opacity = "0";
				    document.getElementById("alert-addPlaylist").style.visibility = "hidden";
				}, 1800);
			},
			error:function(){
				alert("erro ao conectar com servidor");
			}
		});

	});
	$('#form_playlist').submit(function(event){
		var this_form = $(this);
		var aud = this_form.attr('aud');
		var dados = this_form.serialize();
		$.ajax({
			url: '/channel/playlist_add_play',
			type:'GET',
			beforeSend:function(){
			},
			data:dados+'&aud='+aud,
			dataType:'json',
			async:true,
			success:function(json){
				$("#alert-addPlaylist").html(json.message);
				document.getElementById("alert-addPlaylist").style.visibility = "visible";
				document.getElementById("alert-addPlaylist").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-addPlaylist").style.opacity = "0";
				    document.getElementById("alert-addPlaylist").style.visibility = "hidden";
				}, 1800);
				$('#play_load').html(json.html);
				$('#createPlaylist').modal('hide');
			},
		});

		return false;
	});

});
