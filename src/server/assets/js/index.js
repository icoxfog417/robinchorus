
var guide = new Vue({
    el: "#guide",
    data: {
        group:"",
        groupInfo:null,
        validation: {
            group: true
        }
    },
    methods: {
        createGroup: function(){
            var self = this;
            $.post(SCRIPT_ROOT + "/_group",{ group:$("#group").val() },function(data){
                if(data == ""){
                    self.validation.group = false;
                }else{
                    self.validation.group = true;
                    self.groupInfo = data;
                }
            });
        },
        isCreated: function(){
            return (this.groupInfo == null) ? false : true;
        },
        qrCode: function(){
            if(this.isCreated){
                return "http://chart.apis.google.com/chart?chs=150x150&cht=qr&chl=" + this.groupInfo.url;
            }else{
                return "";
            }
        }
    }
})