$('document').ready( function(){
	$("#audio").change(function(){
		$("#formulario_audio").submit();
	});

	$("#foto").change(function(){
		 $('#formulario_foto').submit();		
	});

});