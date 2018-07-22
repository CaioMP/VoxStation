$('document').ready( function(){
	$('.btn-sintonizar').on('click',function(){
		console.log('disparo funciona')
		var this_ = $(this);
		$.ajax({
			url: this_.attr('url_'),
			type:'GET',
			beforeSend:function(){
				this_.html("atualizando...");
			},
			dataType:'json',
			async:true,
			data:{'canal':this_.attr('id')},
			success:function(json){
				console.log(json);
				this_.text(json.estado);
				this_.attr('style',json.fundo);
				this_.text(json.message);
			},
			error:function(){
				alert("fudeu bahia");
			}
		});
	});
});