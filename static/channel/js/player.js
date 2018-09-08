$(document).ready(function() {
    $('#audio-player').mediaelementplayer({
        alwaysShowControls: true,
        features: ['playpause','volume','progress'],
        audioVolume: 'vertical',
    });

    var autplay = true;

    $("#autoplayOff").click(function() {
        document.getElementById('autoplay').style.display = "inline-block";
        document.getElementById('autoplayOff').style.display = "none";
        autplay = true;
        return autplay;
    });

    $("#autoplay").click(function() {
        document.getElementById('autoplay').style.display = "none";
        document.getElementById('autoplayOff').style.display = "inline-block";
        autplay = false;
        return autplay;
    });

    $('#audio-player').on('ended', function() {
       if (autplay) {
           console.log("audio acabou");
           document.getElementById('proximo').click();
       }
       else {
        console.log("autoplay desativado");
       }
    });
});

function descartarAudio() {
    document.getElementById('id_conteudo').value = "";
}

function hideHeader() {
    document.getElementById('header').style.transform = "translateY(-100%)";
    document.getElementById('hideHeader').style.visibility = "hidden";
    document.getElementById('hideHeader').style.opacity = "0";
    document.getElementById('showHeader').style.visibility = "visible";
    document.getElementById('showHeader').style.opacity = "1";
    if (document.getElementById('showAudiosPl')) {
        document.getElementById('showAudiosPl').style.visibility = "hidden";
    }
}

function showHeader() {
    document.getElementById('header').style.transform = "translateY(0)";
    document.getElementById('hideHeader').style.visibility = "visible";
    document.getElementById('hideHeader').style.opacity = "1";
    document.getElementById('showHeader').style.visibility = "hidden";
    document.getElementById('showHeader').style.opacity = "0";
    if (document.getElementById('showAudiosPl')) {
        document.getElementById('showAudiosPl').style.visibility = "visible";
    }
}

function showFooter() {
    document.getElementById('footer').style.opacity = "1";
    document.getElementById('hideHeader').style.opacity = "1";
    document.getElementById('showHeader').style.opacity = "1";
    document.getElementById('hideHeader').style.opacity = "1";
    if (document.getElementById('showAudiosPlIcon')) {
        document.getElementById('showAudiosPlIcon').style.opacity = "1";
    }
}

function hideFooter() {
    document.getElementById('footer').style.opacity = "0";
    document.getElementById('showHeader').style.opacity = "0";
    document.getElementById('hideHeader').style.opacity = "0";
    if (document.getElementById('showAudiosPlIcon')) {
        document.getElementById('showAudiosPlIcon').style.opacity = "0";
    }
}

function showDescription() {
    document.getElementById('descBox').style.display = "block";
    document.getElementById('showDescription').style.visibility = "hidden";
    document.getElementById('hideDescription').style.visibility = "visible";
}

function hideDescription() {
    document.getElementById('descBox').style.display = "none";
    document.getElementById('hideDescription').style.visibility = "hidden";
    document.getElementById('showDescription').style.visibility = "visible";
}

function randomAudios() {
    document.getElementById('random').style.display = "inline-block";
    document.getElementById('offRandom').style.display = "none";

    document.getElementById('randomize').value = "true";
    $("#randomizeForm").submit();
}

function offRandomAudios() {
    document.getElementById('random').style.display = "none";
    document.getElementById('offRandom').style.display = "inline-block";
}

window.addEventListener('click', function(e){
  if (document.getElementById('lb_comentar').contains(e.target)){
    document.getElementById('comment').style.display = "block";
  } else{
    document.getElementById('comment').style.display = "none";
  }
});

/*Mostra o botão de responder ao passar o mouse em cima do comentário*/
function showOpc(id) {
    var responder = document.getElementById(id).getElementsByClassName("resposta")[0].style.display;
    if (responder != "block") {
        document.getElementById(id).getElementsByClassName("responder")[0].style.display = "block";
    }
}

/*Esconde o botão de responder ao tirar o mouse do comentário*/
function hideOpc(id) {
    var responder = document.getElementById(id).getElementsByClassName("resposta")[0].style.display;
    if (responder != "block") {
        document.getElementById(id).getElementsByClassName("responder")[0].style.display = "none";
    }
}

function showResponder(parentElement) {
    /*Não permitir que mais de uma resposta seja dada ao mesmo tempo*/
    var x_all = document.getElementsByClassName("resposta");
    var resposta_all = document.getElementsByClassName("responder");
    var responder = document.getElementsByClassName("responder");
    for (var i=0; i<x_all.length; i++){
        x_all[i].style.display = "none";
        resposta_all[i].innerHTML = "Responder";
        responder[i].style.display = "none";
    }

    document.getElementById(parentElement).getElementsByTagName("TEXTAREA")[0].value = "";
    document.getElementById(parentElement).getElementsByClassName("responder")[0].innerHTML = "Limpar";
    document.getElementById(parentElement).getElementsByClassName("responder")[0].style.display = "block";

    /*Habilita a parte de responder*/
    var x = document.getElementById(parentElement).getElementsByClassName("resposta");
    x[0].style.display = "block";
}

function closeResponder() {
    var resposta = document.getElementsByClassName("responder");
    var x = document.getElementsByClassName("resposta");

    for (var i=0; i<x.length; i++){
        x[i].style.display = "none";
        resposta[i].innerHTML = "Responder";
    }
}

function showRespostas(parentElement) {
    x = document.getElementById(parentElement).getElementsByClassName("respostas");
    for (var i=0; i<x.length; i++){
        x[i].style.display = "block";
    }

    document.getElementById(parentElement).getElementsByClassName("ver")[0].style.display = "none";
    document.getElementById(parentElement).getElementsByClassName("esconder")[0].style.display = "block";
}

function hideRespostas(parentElement) {
    x = document.getElementById(parentElement).getElementsByClassName("respostas");
    for (var i=0; i<x.length; i++){
        x[i].style.display = "none";
    }

    document.getElementById(parentElement).getElementsByClassName("ver")[0].style.display = "block";
    document.getElementById(parentElement).getElementsByClassName("esconder")[0].style.display = "none";
}

