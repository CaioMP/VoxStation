$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
        $('#sideFade').toggleClass('fadeActive');
    });

    $('#sideFade').on('click', function () {
        $('#sidebar').addClass('active');
        $('#sidebarCollapse').addClass('active');
        $(this).removeClass('fadeActive');
    })

    $('[rel="tooltip"]').tooltip();
    $('[rel="tooltip').on('click', function () {
        $(this).tooltip('hide');
    });

    var prevScrollpos = window.pageYOffset;

    window.onscroll = function() {
        var currentScrollPos = window.pageYOffset;
        if (prevScrollpos > currentScrollPos) {
            document.getElementById("navbar").style.transform = "translateY(0)";
        } else {
            if(window.innerWidth > 575){
                if(currentScrollPos > 70){
                    document.getElementById("navbar").style.transform = "translateY(-104%)";
                    if(!$("#sidebar").hasClass("active")){
                        $("#sidebarCollapse").click();
                    }
                }
            }
            if(window.innerWidth < 576){
                if(currentScrollPos > 140){
                    document.getElementById("navbar").style.transform = "translateY(-104%)";
                    if(!$("#sidebar").hasClass("active")){
                        $("#sidebarCollapse").click();
                    }
                }
            }
            if(window.innerWidth < 415){
                if(currentScrollPos > 110){
                    document.getElementById("navbar").style.transform = "translateY(-104%)";
                    if(!$("#sidebar").hasClass("active")){
                        $("#sidebarCollapse").click();
                    }
                }
            }

        }
        prevScrollpos = currentScrollPos;
    }
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function verificaLogado(logado) {
    if (logado == "False"){
        window.location.href = "/login/";
        $("#reportLink").attr("href", "/login/");
        $('#addToPlaylistLink').removeAttr('data-toggle');
        $('#addToPlaylistLink').removeAttr('data-target');
        $("#addToPlaylistLink").attr("href", "/login/");
    }
    else{
        $("#reportLink").attr("data-toggle", "modal");
        $("#reportLink").attr("data-target", "#reportAudio");
    }
}

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

//Mostrar o botão de configurações na imagem do dropdown-item de favoritos
function showDelFav(id){
    document.getElementById(id).getElementsByClassName("btn-delFav")[0].style.opacity = ".9";
}

//Esconde o botão de play na configurações do dropdown-item de favoritos
function hideDelFav(id){
    document.getElementById(id).getElementsByClassName("btn-delFav")[0].style.opacity = "0";
}