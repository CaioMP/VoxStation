$(function(){
	$('#id_capa').change(function(){
		const file = $(this)[0].files[0]
		const fileReader = new FileReader()
		fileReader.onloadend = function(){
		    if($('#error_capa').length){
		        document.getElementById("error_capa").style.display = "none";
		    }
			$('#foto-default').attr('src',fileReader.result)
		}
		fileReader.readAsDataURL(file)
	})
})
