$('document').ready( function(){
	$('#form_chan_edit').submit(function(event){
		console.log("submitado");
		var this_form = $(this);
		var dados = this_form.serialize();
		$.ajax({
			url: this_form.attr('cn_'),
			type:'GET',
			beforeSend:function(){
			},
			data:dados,
			dataType:'json',
			async:true,
			success:function(json){
				$('#nome_canal').text(json.nome);
				$("#alert-addPlaylist").html(json.message);
				document.getElementById("alert-addPlaylist").style.visibility = "visible";
				document.getElementById("alert-addPlaylist").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-addPlaylist").style.opacity = "0";
				    document.getElementById("alert-addPlaylist").style.visibility = "hidden";
				}, 1800);
				window.location.reload();

			},
			error:function(){
				alert("erro no servidor");
			}
		});

		return false;
	});
});