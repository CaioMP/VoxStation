document.addEventListener('DOMContentLoaded', function() {
    const webSocketBridge = new channels.WebSocketBridge();
    const nl = document.querySelector("#notifylist");

    webSocketBridge.connect('/notifications/');
    webSocketBridge.listen(function(action, stream) {
        console.log("RESPONSE:", action, "STREAM:", stream);
        if(action.event == "New Audio") {
            if(document.getElementById('notificNumber').style.display == "none"){
                $('#notificNumber').html('1');
                document.getElementById('notificNumber').style.display = "block";
            }
            else{
                var n = parseInt($('#notificNumber').html());
                $('#notificNumber').html(n+1);
            }

            if($("#noNotific").length) {
                document.getElementById('noNotific').style.display = "none";
            }

            var link = document.createElement("a");
            link.setAttribute('href', action.link);

            var el = document.createElement("li");
            el.classList.add("dropdown-item");
            el.classList.add("dropdown-item-custom");

            var canal = document.createElement("img");
            canal.setAttribute('src', action.canal);
            canal.setAttribute('class', 'channel-notific');

            var capa = document.createElement("img");
            capa.setAttribute('src', action.capa);
            capa.setAttribute('class', 'audio-notific');

            var titulo = document.createElement("h5");
            titulo.innerHTML = action.titulo;

            var data = document.createElement("h3");
            data.innerHTML = action.data;

            link.appendChild(canal);
            link.appendChild(capa);
            link.appendChild(titulo);
            link.appendChild(data);
            el.appendChild(link);
            nl.prepend(el);
        }
    })
    document.ws = webSocketBridge;
})