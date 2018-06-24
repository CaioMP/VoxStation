//Função para fechar o alert depois de um tempo
window.setTimeout(function() {
    $(".alert").fadeTo(250, 0).slideUp(250, function(){
        $(this).remove();
    });
}, 1800);

function showAlert(){
    $(".fade").addClass("in")
}

$(document).ready(function() {
    showAlert();  //Função que para colocar efeito de fade no alert do erro
});