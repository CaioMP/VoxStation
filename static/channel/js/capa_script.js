$(function(){
	$('#id_capa').change(function(){
		const file = $(this)[0].files[0]
		const fileReader = new FileReader()
		fileReader.onloadend = function(){
			$('#foto-default').attr('src',fileReader.result)
		}
		fileReader.readAsDataURL(file)
	})
})