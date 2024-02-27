function getChatSocketUrl(reciever_id) {
    if (document.location.protocol == 'https:') {
        return 'wss://' + window.location.host + '/ws/' + reciever_id + '/'
    }
    else {
        return 'ws://' + window.location.host + '/ws/' + reciever_id + '/'
    }
}

var userSocket; 
function createSocket(sockerUrl){
    userSocket = new WebSocket(sockerUrl);
    return userSocket;
}

function connectToSocket(reciever_id){
    var socketUrl = getChatSocketUrl(reciever_id);
    userSocket = createSocket(socketUrl);
}