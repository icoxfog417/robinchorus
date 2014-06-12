var chats = new Vue({
    el: "#chats",
    data:{
        chats: []
    },
    created: function () {
        socket = CHANNEL.open();
        socket.onopen = this.onOpen;
        socket.onmessage = this.onMessage;
        socket.onerror = this.onError;
        socket.onclose = this.onClose;
        this.init();
    },
    methods: {
        onOpen: function(){
            console.log("socket open!");
        },
        onMessage: function(envelope){
            var c = JSON.parse(envelope.data);
            chats.$data.chats.unshift(c);
        },
        onerror: function(){
            console.log("error occur");
        },
        onClose: function(){
            console.log("close connection");
        },
        init: function(){
            var self = this;
            $.getJSON(SCRIPT_ROOT + "/_find",function(data){
                if(data !== undefined || data != ""){
                    self.chats.$remove();
                    for(var i = 0; i < data.chats.length;i++){
                        self.chats.push(data.chats[i]);
                    }
                }
            });
        },
        feature: function(e){
            $(e.target).toggleClass("feature");
        },
        sendMessage: function(e){
            var self = this;
            var msg = $("#message").val();
            if(msg == ""){
                return false;
            }else{
                $.post(SCRIPT_ROOT ,{message:msg},function(data){
                    // clear message on the text box. message is sended by channel (invoke onMessage method)
                    $("#message").val("");
                })
            }

        }
    }
})

$(function(){
    $("#send").click(function(e){
        chats.sendMessage(e);
    })

    function resize(){
        var chatHeight = $(window).height() - 210;
        $("#chats").height(chatHeight);
    }

    $(window).resize(resize)
    resize();

})