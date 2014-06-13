var chats = new Vue({
    el: "#chats",
    data:{
        chats: [],
        stamps: []
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
            //load chats
            $.getJSON(SCRIPT_ROOT + "/_find",function(data){
                if(data !== undefined || data != ""){
                    self.chats.$remove();
                    data.chats.forEach(function(c){ self.chats.push(c); })
                }
            });

            //load stamp images
            $.post(SCRIPT_ROOT + "/_stamps" ,function(data){
                self.stamps.$remove();
                data.stamps.forEach(function(s){ self.stamps.push(s); })
            })

        },
        feature: function(e){
            $(e.target).toggleClass("feature");
        },
        sendMessage: function(e){
            var msg = $("#message").val();
            this.send("text",msg, function(data){
                // clear message on the text box. message is sended by channel (invoke onMessage method)
                $("#message").val("");
            });
        },
        sendStamp: function(e){
            var stamp = $(e.target).attr("src");
            this.send("stamp",stamp, function(data){
                $("#stamps").hide();
            });
        },
        send: function(type, msg, callback){
            var self = this;
            if(msg == ""){
                return false;
            }else{
                $.post(SCRIPT_ROOT ,{type:type, message:msg},callback);
            }
        }

    }
})

$(function(){
    //handle footer event and pass it to view model
    $("#send").click(function(e){
        chats.sendMessage(e);
    })

    $("#showStamp").click(function(e){
        $("#stamps").toggle();
    })

    function resize(){
        var chatHeight = $(window).height() - 210; //minus header/footer height
        $("#chats").height(chatHeight);
    }
    $(window).resize(resize)
    resize();

})