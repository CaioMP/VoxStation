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
				if(json.estado == "Sintonizar") {
				    if(document.getElementById("formNotificMe").length){
				        document.getElementById("formNotificMe").style.opacity = "0";
				        document.getElementById("formNotificMe").style.visibility = "hidden";
				    }
				}
				else {
				    document.getElementById("formNotificMe").style.opacity = "1";
				    document.getElementById("formNotificMe").style.visibility = "visible";
				}

				this_.text(json.estado);
				this_.css('background',json.cor);
				$('#num_seg').text(json.num_seg);
				window.setTimeout(function() {
                    $('#no-notific').removeClass('active-notific');
                    $('#notific').addClass('active-notific');
                }, 500);
			},
		});
	});
});