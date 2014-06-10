
var chat = new Vue({
    el: "#chat",
    data:{
        chats: []
    },
    created: function () {
        socket = CHANNEL.open();
        socket.onopen = this.onOpen;
        socket.onmessage = this.onMessage;
        socket.onerror = this.onError;
        socket.onclose = this.onClose;
        this.init():
    },
    methods: {
        onOpen: function(){
            alert("socket open!");
        },
        onMessage: function(data){
            alert("message receive!");
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
                if(data != ""){
                    chats = [];
                    chats.push(data);
                }
            });
        }
    }
})
