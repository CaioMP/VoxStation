$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
    });

    $('[rel="tooltip"]').tooltip();
    $('[rel="tooltip').on('click', function () {
        $(this).tooltip('hide');
    });
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

//Salva as alterações
function Submit() {
    document.getElementById('save').value = document.getElementById('submitForm').value;
    document.getElementById('save').click();
    showAlert();
}

//Função para fechar o alert depois de um tempo
window.setTimeout(function() {
    $(".alert").fadeTo(250, 0).slideUp(250, function(){
        $(this).remove();
    });
}, 1800);

//Efeito fade para o alert
function showAlert(){
    $(".fade").addClass("in")
}

//Identificar quando as notificações foram visualizadas
function Visualized(){
    document.getElementById("notificNumber").style.display="none";
    $("#formNotific").submit();
}
