function showDelete(parentElement) {
    document.getElementById(parentElement).getElementsByClassName("delete")[0].style.visibility = "visible";
    document.getElementById(parentElement).getElementsByClassName("delete")[0].style.opacity = "1";
    document.getElementById(parentElement).getElementsByClassName("numero-audio")[0].style.visibility = "hidden";
    document.getElementById(parentElement).getElementsByClassName("numero-audio")[0].style.opacity = "0";
}

function hideDelete(parentElement) {
    document.getElementById(parentElement).getElementsByClassName("delete")[0].style.visibility = "hidden";
    document.getElementById(parentElement).getElementsByClassName("delete")[0].style.opacity = "0";
    document.getElementById(parentElement).getElementsByClassName("numero-audio")[0].style.visibility = "visible";
    document.getElementById(parentElement).getElementsByClassName("numero-audio")[0].style.opacity = "1";
}

function showDescription() {
    document.getElementById('desc').style.display = "block";
    document.getElementById('showDescription').style.display = "none";
    document.getElementById('hideDescription').style.display = "block";
}

function hideDescription() {
    document.getElementById('desc').style.display = "none";
    document.getElementById('hideDescription').style.display = "none";
    document.getElementById('showDescription').style.display = "block";
}


function savePlaylist() {
    $("#formSavePl").submit();
}