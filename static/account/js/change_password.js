$(document).ready(function(){
    $("#modal-password").modal("show"); //Mostra o modal ao carregar a página
    checkError(); //Função de verificar erros nos campos
});

function checkError() {
    //Verifica se há um erro no campo 'Senha antiga'
    if (document.getElementById("error-old_password").style.display != "none") {
        document.getElementById("id_old_password").style.borderColor = "darkred";
        document.getElementById("old_password").style.color = "darkred";
    }

    //Verifica se há um erro no campo 'Nova senha'
    if (document.getElementById("error-new_password1").style.display != "none") {
        document.getElementById("id_new_password1").style.borderColor = "darkred";
        document.getElementById("new_password1").style.color = "darkred";
    }

    //Verifica se há um erro no campo 'Digite-a novamente'
    if (document.getElementById("error-new_password2").style.display != "none") {
        document.getElementById("id_new_password2").style.borderColor = "darkred";
        document.getElementById("new_password2").style.color = "darkred";
    }
}