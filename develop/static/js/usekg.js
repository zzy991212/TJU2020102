contentHook = function(item){
    return "<div>"+item.name+"</div>"
}

$(function () {
    $('.tryjson').ready(function () {
        var u = document.forms[0].elements["val"].value;
        $.ajax({
            url: '/returnjson',
            type: 'get',
            success: function (data) {
                $('.tryjson').html("加载成功");
                $("svg").remove()
                var config = {
                    content: null,
                    contentHook:contentHook,
                    nodeColor: null,
                    linkColor: null,
                    width: 490,
                    height: 500
                }
                initKG(data, config, "#mountNode") // mountNode为容器名
            }
        })
    })
});
