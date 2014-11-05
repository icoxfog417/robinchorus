var SCRIPT_ROOT = [location.protocol, "//", location.host, location.pathname].join("");
if(SCRIPT_ROOT.substring(SCRIPT_ROOT.length - 1) == "/"){
    SCRIPT_ROOT = SCRIPT_ROOT.slice(0,-1);
}
Vue.config({
    delimiters: ["[", "]"]
});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$.ajaxSetup({
    data: {
        _xsrf: getCookie("_xsrf"),
    }
});
