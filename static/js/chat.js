var chats = new Vue({
    el: "#chats",
    data:{
        chats: [],
        stamps: {},
        reference: "",
        sort_field: "created_at",
        sort_reverse: true,
        filter: ""
    },
    created: function () {
        var socket = null;
        var url = [(location.protocol == "https:")? "wss:" : "ws:", "//", location.host, location.pathname, "/socket"].join("");
        socket = new ReconnectingWebSocket(url);
        socket.onopen = this.onOpen;
        socket.onmessage = this.onMessage;
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
                if(chatArray[i].key == c.key){
                    storedAt = i;
                    break;
                }
            }

            if(storedAt > -1){
                //chatArray.splice(storedAt,1,c); //update
                chatArray[storedAt].like = c.like;
            }else{
                chatArray.unshift(c);
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
            $.getJSON(SCRIPT_ROOT + "/chats",function(data){
                if(Object.keys(data).length > 0){
                    self.chats.$remove();
                    data.chats.forEach(function(c){ self.chats.push(c); });
                    $("#chats").css("visibility","visible")
                }
            });

            //load stamp images
            $.getJSON(SCRIPT_ROOT + "/stamps" ,function(data){
                self.stamps = {};
                for(var key in data.stamps){
                    var stampKey = key.charAt(0).toUpperCase() + key.slice(1); //upper first character
                    self.stamps[stampKey] = [];
                    data.stamps[key].forEach(function(s){ self.stamps[stampKey].push(s); })
                }
            })

        },
        feature: function(e){
            $(e.target).toggleClass("feature");
        },
        orderByCreated: function(e){
            this.sort_field = "created_at";
        },
        orderByLike: function(e){
            this.sort_field = "like";
        },
        sendMessage: function(e){
            var msg = $("#message").val();
            this.send("text",msg, function(data){
                // clear message on the text box. message is sended by channel (invoke onMessage method)
                $("#message").val("");
                $(".refereed").removeClass("refereed")
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
            $.ajax({type: "PUT", url: SCRIPT_ROOT, data: {type:"like", key:c.key}});
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
            if($("#" + c.key).hasClass("refereed")){
                $("#message").data("reference","");
                $("#" + c.key).removeClass("refereed")
            }else{
                $("#message").data("reference",c.key);
                $("#" + c.key).addClass("refereed");
                $("#message").focus();
            }
            return false;
        },
        refer: function(vm){
            var self = this;

            //set visibility
            if(self.filter != vm.key){
                self.chats.forEach(function(c){ c.visible = "0" })

                var ref = vm.key;
                while(ref){
                    var ref_base = ref;
                    ref = "";
                    self.chats.forEach(function(c){
                        if(c.key == ref_base){
                            c.visible = "1";
                            ref = c.reference;
                        }
                    });
                }
                self.filter = vm.key;
            }else{
                self.chats.forEach(function(c){ c.visible = "1" })
                self.filter = "";
            }
        }
    },
    filters: {
        marked: marked
    }
})

$(function(){
    //handle footer event and pass it to view model
    $("#send").click(function(e){
        chats.sendMessage(e);
    })

    $("#showStamp").click(function(e){
        $("#stamps").toggle();
        if($("#stamps .active").size() == 0){
            $("#stamps a:first").tab("show");
        }
    })

    function resize(){
        var chatHeight = $(window).height() - 210; //minus header/footer height
        $("#chat-area").height(chatHeight);
    }
    $(window).resize(resize)
    resize();

})