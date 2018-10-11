$('document').ready( function(){
	$('.removeH').on('click',function(){
		var this_ = $(this);
		var id = "card"+this_.attr('id');
		$.ajax({
			url: this_.attr('url_'),
			type:'GET',
			beforeSend:function(){
				document.getElementById(id).style.display = "none";
			},
			dataType:'json',
			async:true,
			data:{},
			success:function(json){
				console.log(json);
				$("#alert-addPlaylist").html(json.message);
				document.getElementById("alert-addPlaylist").style.visibility = "visible";
				document.getElementById("alert-addPlaylist").style.opacity = "1";
				window.setTimeout(function() {
				    document.getElementById("alert-addPlaylist").style.opacity = "0";
				    document.getElementById("alert-addPlaylist").style.visibility = "hidden";
				}, 1800);
			},
		});
	});
});
