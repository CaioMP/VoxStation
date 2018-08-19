/*Esconde os canais da pesquisa*/
function hideChannels() {
    document.getElementById("channels").style.display = "none";
    document.getElementById("hideChannels").style.display = "none";
    document.getElementById("showChannels").style.display = "block";
    document.getElementById("filter-canais").style.display = "none";
    document.getElementById("subChannel").style.color = "initial";
}

/*Mostra os canais da pesquisa*/
function showChannels() {
    document.getElementById("channels").style.display = "block";
    document.getElementById("hideChannels").style.display = "block";
    document.getElementById("showChannels").style.display = "none";
    document.getElementById("filter-canais").style.display = "inline";
    document.getElementById("subChannel").style.color = "#032854";
}

/*Esconde os audios da pesquisa*/
function hideAudios() {
    document.getElementById("audios").style.display = "none";
    document.getElementById("hideAudios").style.display = "none";
    document.getElementById("showAudios").style.display = "block";
    document.getElementById("filter-audios").style.display = "none";
    document.getElementById("filter-duracao").style.display = "none";
    document.getElementById("subAudio").style.color = "initial";
}

/*Mostra os audios da pesquisa*/
function showAudios() {
    document.getElementById("audios").style.display = "block";
    document.getElementById("hideAudios").style.display = "block";
    document.getElementById("showAudios").style.display = "none";
    document.getElementById("filter-audios").style.display = "inline";
    document.getElementById("filter-duracao").style.display = "inline";
    document.getElementById("subAudio").style.color = "#032854";
}

/*Esconde as playlists da pesquisa*/
function hidePlaylists() {
    document.getElementById("playlists").style.display = "none";
    document.getElementById("hidePlaylists").style.display = "none";
    document.getElementById("showPlaylists").style.display = "block";
    document.getElementById("filter-playlists").style.display = "none";
    document.getElementById("subPlaylist").style.color = "initial";
}

/*Mostra as playlists da pesquisa*/
function showPlaylists() {
    document.getElementById("playlists").style.display = "block";
    document.getElementById("hidePlaylists").style.display = "block";
    document.getElementById("showPlaylists").style.display = "none";
    document.getElementById("filter-playlists").style.display = "inline";
    document.getElementById("subPlaylist").style.color = "#032854";
}