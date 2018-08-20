$('document').ready( function(){

	$('.opChan').on('click',function(){
		var this_ = $(this);
		var datas = {'op':this_.attr('val')};
		console.log(datas);
		$.ajax({
			url:$('#caminhoChan').attr('indentifier'),
			type:'GET',
			beforeSend:function(){
				
			},
			dataType:'json',
			async:true,
			data:datas,
			success:function(json){
				$("#chanBox").html(json.html);
				console.log(json.html);
			},
			error:function(){
				
			}
		});
	});

	$('.opAudio').on('click',function(){
		var this_ = $(this);
		var datas = {'op':this_.attr('val')};
		console.log(datas);
		$.ajax({
			url:$('#caminhoAudio').attr('indentifier'),
			type:'GET',
			beforeSend:function(){
				
			},
			dataType:'json',
			async:true,
			data:datas,
			success:function(json){
				$("#audBox").html(json.html);
				console.log(json.html);
			},
			error:function(){
				
			}
		});
	});

	$('.opPlay').on('click',function(){
		var this_ = $(this);
		var datas = {'op':this_.attr('val')};
		console.log(datas);
		$.ajax({
			url:$('#caminhoPlay').attr('indentifier'),
			type:'GET',
			beforeSend:function(){
				
			},
			dataType:'json',
			async:true,
			data:datas,
			success:function(json){
				$("#plBox").html(json.html);
			},
			error:function(){
				
			}
		});
	});





});