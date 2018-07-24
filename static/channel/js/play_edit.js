$('document').ready( function(){
	$('#form_play').submit(function(event){
		console.log("submitado");
		var this_form = $(this);
		var playlist = this_form.attr('play');
		var dados = this_form.serialize();
		$.ajax({
			url: this_form.attr('url_'),
			type:'GET',
			beforeSend:function(){
			},
			data:dados+'&id='+playlist,
			dataType:'json',
			async:true,
			success:function(json){
				$('#play_titul').text(json.message);
				console.log(json.desc);
				$('#desc').html(json.desc);
				$('#desc_edit').hide();
				$('.modal').modal('hide');
			},
			error:function(){
				alert("fudeu bahia");
			}
		});

		return false;
	});
});