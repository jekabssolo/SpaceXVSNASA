function ajaxGET(path, callback){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState==4&&this.status===200){
            callback(this.response);
        }
    }
    request.open("GET", path);
    request.send();
}

function ajaxPOST(path, data, callback){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState==4&&this.status===200){
            callback(this.response);
        }
    }
    request.open("POST", path);
    request.send(data);
}