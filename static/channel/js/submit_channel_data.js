$('document').ready( function(){
	console.log('slve crrraiiiiiiiiiiiiiiiiiii');

	$("#audio").change(function(){
		console.log("mudou");
		$("#formulario_audio").submit();
	});

	$("#foto").change(function(){
		 $('#formulario_foto').submit();		
	});

});