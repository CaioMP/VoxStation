$('document').ready( function(){
	console.log("pinto");
	$('.removeH').on('click',function(){
		var this_ = $(this);
		$.ajax({
			url: this_.attr('url_'),
			type:'GET',
			beforeSend:function(){
				this_.destroy();
			},
			dataType:'json',
			async:true,
			data:{},
			success:function(json){
				console.log(json);
				document.getElementById("alert-addPlaylist").style.visibility = "visible";
				document.getElementById("alert-addPlaylist").style.opacity = "1";
				window.setTimeout(function(){
				    document.getElementById("alert-addPlaylist").style.opacity = "0";
				    document.getElementById("alert-addPlaylist").style.visibility = "hidden";
				}, 1800);
			},
			error:function(){
				alert("erro ao conectar com servidor");
			}
		});
	});
});