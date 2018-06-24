/*Preview dos arquivos de imagem*/
/*Caso o usuário não tenha foto de perfil*/
$(function(){
	$('#troca-foto').change(
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
	$('#troca-foto').change(
	function(){
		const file = $(this)[0].files[0]
		const fileReader = new FileReader()
		fileReader.onloadend = function(){
			$('#foto_perfil').attr('src',fileReader.result)
		}
		fileReader.readAsDataURL(file)
	})
})

//Função para fechar o alert depois de um tempo
window.setTimeout(function() {
    $(".alert").fadeTo(250, 0).slideUp(250, function(){
        $(this).remove();
    });
}, 1800);

$(document).ready(function() {
    checkError();//Função de verificar erros nos campos
});

//Efeito fade para o alert
function showAlert(){
    $(".fade").addClass("in")
}

//Muda o idioma imediatamente
function changeLang() {
    document.getElementById('toSubmit').value = document.getElementById('lang').value;
    document.getElementById('langSubmit').click();
}

//Salva as alterações
function Submit() {
    document.getElementById('save').value = document.getElementById('submitForm').value;
    document.getElementById('save').click();
    showAlert();
}

//Mudar o input em caso de erro
function checkError() {
    //Verifica se há um erro no campo 'Email'
    if ($("#error-email").is(":visible")) {
        document.getElementById("id_email").style.borderColor = "darkred";
        document.getElementById("email").style.color = "darkred";
    }

    //Verifica se há um erro no campo 'Telefone'
    if ($("#error-phone").is(":visible")) {
        document.getElementById("id_phone").style.borderColor = "darkred";
        document.getElementById("id_phone").style.marginBottom = "-27px";
        document.getElementById("phone").style.color = "darkred";
    }

    //Verifica se há um erro no campo 'Primeiro nome'
    if ($("#error-first_name").is(":visible")) {
        document.getElementById("id_first_name").style.borderColor = "darkred";
        document.getElementById("first_name").style.color = "darkred";
    }

    //Verifica se há um erro no campo 'Sobrenome'
    if ($("#error-last_name").is(":visible")) {
        document.getElementById("id_last_name").style.borderColor = "darkred";
        document.getElementById("last_name").style.color = "darkred";
    }

    //Verifica se há um erro no campo 'Nome de Usuário'
    if ($("#error-username").is(":visible")) {
        document.getElementById("id_username").style.borderColor = "darkred";
        document.getElementById("username").style.color = "darkred";
    }
}