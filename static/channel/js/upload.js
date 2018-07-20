$(document).ready(function() {
	$('#form-up').submit(function(e){
		if($('#id_audio').val()){
			e.preventDefault();
			$('.progress').show();
			$(this).ajaxSubmit({
				beforeSubmit:function(){
						
				},
				uploadProgress:function(event, position, total, percentComplete){
					$('.progress-bar').width(percentComplete+'%');
					$('.progress-bar').html('<div id="progress-status">'+percentComplete+' %</div>');
				},
				sucess:function(){
					window.setTimeout(function(){ 
    					$('#progress-status').text('uploaded');
					}, 3000);
					$('.progress').hide();
				},
				resetForm:true;
			})
			return false;
		}
	})
});