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
