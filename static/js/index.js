
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
            $.post(SCRIPT_ROOT + "/group",{ groupName:$("#groupName").val() },function(data){
                if(Object.keys(data).length == 0){
                    self.validation.groupName = false;
                }else{
                    self.validation.groupName = true;
                    self.groupInfo = data;
                    self.groupInfo.url = location.protocol + self.groupInfo.url;
                    $("#qrcode").qrcode({width: 150, height: 150, text: self.groupInfo.url});
                }
            });
        },
        isCreated: function(){
            return (this.groupInfo == null) ? false : true;
        }
    }
})