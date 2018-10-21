$(document).ready(function() {
    //Verifica se há um erro no campo 'Nome de Usuário'
    if ($("#error-name").is(":visible")) {
        document.getElementById("id_nome_canal").style.borderColor = "darkred";
        document.getElementById("id_nome_canal").style.marginBottom = "18px";
        document.getElementById("nome").style.color = "darkred";
    }
});

/*Preview dos arquivos de imagem*/
/*Caso o usuário não tenha foto de perfil*/
$(function(){
	$('#foto-canal').change(
	function(){
		const file = $(this)[0].files[0]
		const fileReader = new FileReader()
		fileReader.onloadend = function(){
			$('#foto').attr('src',fileReader.result)
		}
		fileReader.readAsDataURL(file)
	})
})

/*Caso o usuário tenha uma foto de perfil*/
$(function(){
	$('#foto-canal').change(
	function(){
		const file = $(this)[0].files[0]
		const fileReader = new FileReader()
		fileReader.onloadend = function(){
			$('#foto_perfil').attr('src',fileReader.result)
		}
		fileReader.readAsDataURL(file)
	})
})

/*Preview da capa do canal*/
$(function(){
	$('#fundo').change(
	function(){
		const file = $(this)[0].files[0]
		const fileReader = new FileReader()
		fileReader.onloadend = function(){
		    src = 'url('+fileReader.result+')';
		    document.getElementById("capa").style.backgroundImage = src;
		}
		fileReader.readAsDataURL(file)
	})
})

/*Mostra e esconde os icones dentro dos buttons*/
function mostrarIcone() {
    document.getElementById("icon").style.visibility = "visible";
}

function esconderIcone() {
    document.getElementById("icon").style.visibility = "hidden";
}

