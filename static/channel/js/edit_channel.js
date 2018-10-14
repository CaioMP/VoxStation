$(function(){
	$('#id_capa_tal').change(
	function(){
		const file = $(this)[0].files[0]
		const fileReader = new FileReader()
		fileReader.onloadend = function(){
		    src = 'url('+fileReader.result+')';
		    document.getElementById("capa_preview").style.backgroundImage = src;
		}
		fileReader.readAsDataURL(file)
	})
})

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function hideModalLinks() {
    $('#addLinksChannel').modal('hide');
}

function addRedesSociais() {
    document.getElementById('add-redes-sociais').style.display = "flex";
}

/*Mostra o alert quando um áudio é removido e da submit no form depois*/
function showAlertRemove(audio) {
    document.getElementById("alert-removeAudio").style.visibility = "visible";
    document.getElementById("alert-removeAudio").style.opacity = "1";
    console.log(audio);
    document.getElementById("id_audio_removido").value = audio;
    window.setTimeout(function() {
        document.getElementById("alert-removeAudio").style.opacity = "0";
        document.getElementById("alert-removeAudio").style.visibility = "hidden";
        document.getElementById("id_remove").value = "removido";
        document.getElementById("remove_audio_form").submit();
    }, 1500);
}