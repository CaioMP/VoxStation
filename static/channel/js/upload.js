$(document).ready(function() {
    if($('#infoCreateCanal').length) {
        $('#infoCreateCanal').modal('show');
    }

    error_tag = false;

    $('#id_text').keyup(function(){
        var value = $(this).val();
        if ((value.indexOf('#') == 0) == false && value != '') {
            document.getElementById('error-tag').style.display = "block";
            error_tag = true;
        }
        else {
            document.getElementById('error-tag').style.display = "none";
        }
    })

	$('#form-up').submit(function(e){
		if($('#id_audio').val() && $('#id_capa').val() && error_tag==false){
			e.preventDefault();
			$('.progress').show();
			$(this).ajaxSubmit({
				beforeSubmit:function(){

				},
				uploadProgress:function(event, position, total, percentComplete){
					$('.progress-bar').width(percentComplete+'%');
					$('.progress-bar').html('<div id="progress-status">'+percentComplete+' %</div>');
				},
				success:function(data){
					window.setTimeout(function(){
    					window.location.href = "/";
					}, 500);
				},
				resetForm:true
			})
			return true
		}
	})
	$('#id_audio').change(function(e){
        var fileName = e.target.files[0].name;
        document.getElementById("nameAudio").style.color = "initial";
        $('#nameAudio').html(fileName);
    });
});