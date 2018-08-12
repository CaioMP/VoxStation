$('document').ready( function(){
	$('.op').on('click',function(){
		var this_ = $(this);
		var datas = {'opcao':this_.attr('val')};
		console.log(datas);
		$.ajax({
			url:$('#caminho').attr('identifier'),
			type:'GET',
			beforeSend:function(){
				
			},
			dataType:'json',
			async:true,
			data:datas,
			success:function(json){
				$("#container_audios").html(json.html);
			},
			error:function(){
				
			}
		});
	});
});