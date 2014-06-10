
var guide = new Vue({
    el: "#guide",
    data: {
        groupName:"",
        groupInfo:null,
        validation: {
            groupName: true
        }
    },
    methods: {
        createGroup: function(){
            var self = this;
            $.post(SCRIPT_ROOT + "/_group",{ groupName:$("#groupName").val() },function(data){
                if(data == ""){
                    self.validation.groupName = false;
                }else{
                    self.validation.groupName = true;
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