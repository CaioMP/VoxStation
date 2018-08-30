function showAudiosPl() {
    document.getElementById('infoAudio').style.display = "none";
    document.getElementById('footer').style.display = "none";
    document.getElementById('hideHeader').style.display = "none";
    document.getElementById('showAudiosPl').style.display = "none";
    document.getElementById('header').style.overflow = "auto";
    document.getElementById('playlistAudios').style.display = "block";
}

function hideAudiosPl() {
    document.getElementById('infoAudio').style.display = "block";
    document.getElementById('footer').style.display = "block";
    document.getElementById('hideHeader').style.display = "block";
    document.getElementById('showAudiosPl').style.display = "block";
    document.getElementById('header').style.overflow = "hidden";
    document.getElementById('playlistAudios').style.display = "none";
}