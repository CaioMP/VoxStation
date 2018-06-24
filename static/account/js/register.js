$(document).ready(function() {
    checkError();//Função de verificar erros nos campos
});

function checkError() {
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

    //Verifica se há um erro no campo 'Email'
    if ($("#error-email").is(":visible")) {
        document.getElementById("id_email").style.borderColor = "darkred";
        document.getElementById("email").style.color = "darkred";
    }

    //Verifica se há um erro no campo 'Nome de Usuário'
    if ($("#error-username").is(":visible")) {
        document.getElementById("id_username").style.borderColor = "darkred";
        document.getElementById("username").style.color = "darkred";
    }

    //Verifica se há um erro no campo 'Senha'
    if ($("#error-password1").is(":visible")) {
        document.getElementById("id_password1").style.borderColor = "darkred";
        document.getElementById("password1").style.color = "darkred";
    }

    //Verifica se há um erro no campo 'Confirmação de Senha'
    if ($("#error-password2").is(":visible")) {
        document.getElementById("id_password2").style.borderColor = "darkred";
        document.getElementById("password2").style.color = "darkred";
    }
}