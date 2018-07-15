$('document').ready( function(){
	$('#sintonizar').on('click',function(){
		var this_ = $('#sintonizar')
		$.ajax({
			url: this_.attr('url_'),
			type:'GET',
			beforeSend:function(){
				this_.html("atualizando...");
			},
			dataType:'json',
			async:true,
			data:{},
			success:function(json){
				console.log(json);
				this_.text(json.estado);
				this_.css("backgroundColor","red");
				$('#num_seg').text(json.num_seg);
			},
			error:function(){
				alert("fudeu bahia");
			}
		});
	});
});