var tag_searched;
var tag_splited;
var tag;

$(function(){
    $('#id_text').keyup(function(){
        tag_searched = $('#id_text').val();
        tag_splited = tag_searched.split(' ');
        tag = tag_splited[tag_splited.length-1];

        if(tag.length > 2 && tag.startsWith("#")){
            $.ajax({
                type: "POST",
                url: "/channel/search_tag",
                data: {
                    'search_tag': tag.replace('#', ''),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: SearchTagSuccess,
                dataType: 'html'
            });
        }

        else{
            document.getElementById("tag-searched").style.opacity = "0";
            $("#tag-searched").empty();
        }
    });
});

function SearchTagSuccess(data, textStatus, jqXHR){
    const ul_tags = document.querySelector("#tag-searched");
    $("#tag-searched").empty();

    $.each(JSON.parse(data), function(key, value) {
        var tag_li = $("#tag-searched").text();
        var tag_li_split = tag_li.split("#");
        tag_li_split.shift();

        for(i = 0; i < value.length; i++){
            if(!tag_li_split[i]){
                document.getElementById("tag-searched").style.opacity = "1";

                li = document.createElement("li");
                li.innerHTML = "#" + value[i];

                li.onclick = function () {
                    last_tag = tag_splited[tag_splited.length-1];

                    $("#id_text").val(
                        function(index, value){
                            return value.substr(0, value.length - last_tag.length);
                    })

                    $("#id_text").val($("#id_text").val() + this.innerHTML);
                };

                ul_tags.appendChild(li);
            }
        }
    });
}