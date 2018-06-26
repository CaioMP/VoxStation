$(document).ready(function() {
	$('#form-up').submit(function(e){
		if($('#id_audio').val()){
			e.preventDefault()
			$('.progress').show()
			$(this).ajaxSubmit({
				beforeSubmit:function(){
						$('.progress-bar').width('100%')
				},
				uploadProgress:function(event, position, total, percentComplete){
					$('.progress-bar').width(percentComplete+'%')
					$('.progress-bar').html('<div id="progress-status">'+percentComplete+' %</div>')
				},
				sucess:function(){
					$('#progressBar').hide()
					$('.progress-bar').html('<div id="progress-sfsd">Uploaded</div>')
				},
				resetForm:true
			})
			return true
		}
	})
});