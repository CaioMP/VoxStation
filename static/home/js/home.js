$('document').ready(function(){
    positions_rep = document.getElementById("more_rep").getElementsByClassName("position-audio");
    positions_ava = document.getElementById("best_av").getElementsByClassName("position-audio");

    for(i = 0; i < positions_rep.length; i++){
        positions_rep[i].innerHTML = "#"+(i+1);
    }

    for(i = 0; i < positions_ava.length; i++){
        positions_ava[i].innerHTML = "#"+(i+1);
    }
});

function activeNum(id){
    document.getElementById(id).getElementsByClassName("position-audio")[0].style.backgroundColor = "#0000002e";
}

function changeBgcNum(id){
    document.getElementById(id).getElementsByClassName("position-audio")[0].style.backgroundColor = "rgba(0, 0, 0, 0.04)";
}