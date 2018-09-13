function showAudiosPl() {
    document.getElementById('infoAudio').style.transform = "translateX(110%)";
    document.getElementById('footer').style.transform = "translateX(110%)";
    document.getElementById('hideHeader').style.display = "none";
    document.getElementById('showAudiosPl').style.display = "none";
    document.getElementById('header').style.maxHeight = "100%";
    document.getElementById('playlistAudios').style.marginTop = "0";
    document.getElementById('playlistAudios').style.transform = "translateX(0)";
    document.getElementById('infoAudio').style.display = "none";
    setTimeout(function(){
        document.getElementById('header').style.overflow = "auto";
    }, 500);
}

function hideAudiosPl() {
    document.getElementById('infoAudio').style.transform = "translateX(0)";
    document.getElementById('footer').style.transform = "translateX(0)";
    document.getElementById('hideHeader').style.display = "block";
    document.getElementById('showAudiosPl').style.display = "block";
    document.getElementById('header').style.overflow = "hidden";
    document.getElementById('header').style.maxHeight = "4.3rem";
    document.getElementById('playlistAudios').style.marginTop = "-3rem";
    document.getElementById('playlistAudios').style.transform = "translateX(-110%)";
    document.getElementById('infoAudio').style.display = "block";
}

function randomAudios() {
    document.getElementById('random').style.display = "inline-block";
    document.getElementById('offRandom').style.display = "none";
}

function offRandomAudios() {
    document.getElementById('random').style.display = "none";
    document.getElementById('offRandom').style.display = "inline-block";
}