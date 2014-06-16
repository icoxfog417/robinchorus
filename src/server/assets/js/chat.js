var chats = new Vue({
    el: "#chats",
    data:{
        chats: [],
        stamps: [],
        reference: "",
        sort_field: "created_timestamp",
        sort_reverse: true,
        filter: ""
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
            var chatArray = chats.$data.chats;
            var storedAt = -1;
            for(var i = 0; i < chatArray.length;i++){
                if(chatArray[i].id == c.id){
                    storedAt = i;
                    break;
                }
            }

            if(storedAt > -1){
                chatArray.splice(storedAt,1,c); //update
            }else{
                chatArray.unshift(c);
                if(c.reference){
                    setTimeout(function(){
                        chats.refer(c);
                    },1000);
                }
            }

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
                if(data){
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
        orderByCreated: function(e){
            this.sort_field = "created_timestamp";
        },
        orderByLike: function(e){
            this.sort_field = "like";
        },
        sendMessage: function(e){
            var msg = $("#message").val();
            this.send("text",msg, function(data){
                // clear message on the text box. message is sended by channel (invoke onMessage method)
                $("#message").val("");
                $("#message").data("reference","")
            });
        },
        sendStamp: function(e){
            var stamp = $(e.target).attr("src");
            this.send("stamp",stamp, function(data){
                $("#stamps").hide();
            });
        },
        sendLike: function(c){
            $.post(SCRIPT_ROOT ,{type:"like", id:c.id});
            return false;
        },
        send: function(type, msg, callback){
            var self = this;
            if(msg == ""){
                return false;
            }else{
                var reference = $("#message").data("reference");
                if(reference == "" && self.filter != ""){
                    reference = self.filter;
                }
                $.post(SCRIPT_ROOT ,{type:type, message:msg, reference:reference},callback);
            }
        },
        setReply: function(c){
            $("#message").data("reference",c.id);
            $("#message").focus();
            return false;
        },
        refer: function(vm){
            var self = this;

            //set visibility
            if(self.filter != vm.id){
                self.chats.forEach(function(c){ c.visible = "0" })

                var ref = vm.id;
                while(ref){
                    var ref_base = ref;
                    ref = "";
                    self.chats.forEach(function(c){
                        if(c.id == ref_base){
                            c.visible = "1";
                            ref = c.reference;
                        }
                    });
                }
                self.filter = vm.id;
            }else{
                self.chats.forEach(function(c){ c.visible = "1" })
                self.filter = "";
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
        $("#chat-area").height(chatHeight);
    }
    $(window).resize(resize)
    resize();

})