function hideHeader() {
    document.getElementById('header').style.transform = "translateY(-100%)";
    document.getElementById('hideHeader').style.visibility = "hidden";
    document.getElementById('hideHeader').style.opacity = "0";
    document.getElementById('showHeader').style.visibility = "visible";
    document.getElementById('showHeader').style.opacity = "1";
}

function showHeader() {
    document.getElementById('header').style.transform = "translateY(0)";
    document.getElementById('hideHeader').style.visibility = "visible";
    document.getElementById('hideHeader').style.opacity = "1";
    document.getElementById('showHeader').style.visibility = "hidden";
    document.getElementById('showHeader').style.opacity = "0";
}

function showFooter() {
    document.getElementById('footer').style.opacity = "1";
    document.getElementById('hideHeader').style.opacity = "1";
    document.getElementById('pause').style.opacity = "1";
    document.getElementById('showHeader').style.opacity = "1";
    document.getElementById('hideHeader').style.opacity = "1";
}

function hideFooter() {
    document.getElementById('footer').style.opacity = "0";
    document.getElementById('volume').style.opacity = "0";
    document.getElementById('volume').style.visibility = "hidden";
    document.getElementById('pause').style.opacity = "0";
    document.getElementById('showHeader').style.opacity = "0";
    document.getElementById('hideHeader').style.opacity = "0";
}

function showVolume() {
    document.getElementById('volume').style.visibility = "visible";
    document.getElementById('volume').style.opacity = "1";
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