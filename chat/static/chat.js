// const id = {{request.user.id}};
// const message_username = {{user}};
// const id = JSON.parse(document.getElementById('json-username').textContent);
// const message_username = JSON.parse(document.getElementById('json-message-username').textContent);

function getChatSocketUrl(reciever_id) {
    if (document.location.protocol == 'https:') {
        return 'wss://' + window.location.host + '/ws/' + reciever_id + '/'
    }
    else {
        return 'ws://' + window.location.host + '/ws/' + reciever_id + '/'
    }
}

function getChatSocketUrl(reciever_id) {
    if (document.location.protocol == 'https:') {
        return 'wss://' + window.location.host + '/ws/' + reciever_id + '/'
    }
    else {
        return 'ws://' + window.location.host + '/ws/' + reciever_id + '/'
    }
}

var userSocket;
function createSocket(sockerUrl) {
    userSocket = new WebSocket(sockerUrl);
    return userSocket;
}
function toDataURL(file, callback) {
    var reader = new FileReader();
    reader.onload = function () {
        var dataURL = reader.result;
        callback(dataURL);
    }
    reader.readAsDataURL(file);
}

document.getElementById('chatUploadedFile').addEventListener('change', async function (event) {
    var file = event.target.files[0];
    const base64 = await convertBase64(file);
    localStorage.setItem("userUploadedFile", base64);
    const reciever_id = JSON.parse(document.getElementById('json-username').textContent);
    const send_id = JSON.parse(document.getElementById('json-message-username').textContent);

    toDataURL(file, function (dataURL) {
        userSocket.send(JSON.stringify({
            'type': 'file',
            'fileName': file.name,
            'dataURL': dataURL,
            'username': reciever_id,
            "message": ""
        }))
    })
})
const convertBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file);

        fileReader.onload = () => {
            resolve(fileReader.result);
        };

        fileReader.onerror = (error) => {
            reject(error);
        };
    });
};

function uploadChatFile() {
    document.getElementById("chatUploadedFile").click();

}

$(".chat-history").stop().animate({ scrollTop: $(".chat-history")[0].scrollHeight }, 1000);

const reciever_id = JSON.parse(document.getElementById('json-username').textContent);
const send_id = JSON.parse(document.getElementById('json-message-username').textContent);
console.log(send_id, reciever_id);

var socketUrl = getChatSocketUrl(reciever_id);

if (userSocket == undefined) {
    userSocket = createSocket(socketUrl);
}
userSocket.onopen = function (e) {
    console.log("CONNECTION ESTABLISHED", socketUrl);
}

userSocket.onclose = function (e) {
    console.log("CONNECTION LOST", socketUrl);
}

userSocket.onerror = function (e) {
    console.log("ERROR OCCURED", socketUrl);
}

userSocket.onmessage = function (e) {
    console.log(e.data.message)
    const data = JSON.parse(e.data);
    var today = new Date();
    time_since = timeSince(today);
    if (data.user_id == reciever_id) {
        if(data.message_type == "text"){
            document.querySelector('#chat-body').innerHTML +=
            `  <li class="clearfix">
                                                                <div class="message-data align-right">
                                                                  <span class="message-data-time">${time_since}</span> &nbsp; &nbsp;                                                      
                                                                </div>
                                                                <div class="message other-message float-right">
                                                                    ${data.message}
                                                                </div>
                                                              </li>`
        }
        else {
            document.querySelector('#chat-body').innerHTML +=
            `
            <div class="message other-message float-right"><div class="sender-text">${'<div class="sender_img" style="width: 50%;"><img style="width: 100%;" src=/media/chat_uploads/' + data.file_name + '>'}</div></div>

            `
        }
    }
    //<a download="File1.png" href='+data.file_name+'><img src="../../static/img/icons-download.png" class="download-icon"></a>
    else if (data.message_type == "file_upload") {
        document.querySelector('#chat-body').innerHTML +=
            `
        <div class="message my-message"><div class="sender-text">${'<div class="sender_img" style="width: 50%;"><img style="width: 100%;" src=/media/chat_uploads/' + data.file_name + '>'}</div></div>

        `
    }
    else {
        if (data.message_type == "file_upload") {
            document.querySelector('#chat-body').innerHTML +=
                `
            <div class="sender-text">${'<div class="sender_img" style="width: 50%;"><img style="width: 100%;" src=/media/chat_uploads/' + data.file_name + '>'}</div>
    
            `
        }
        else {
            document.querySelector('#chat-body').innerHTML +=
                ` <li>
                                                                    <div class="message-data">
                                                                    <span class="message-data-time">${time_since}</span>
                                                                    </div>
                                                                    <div class="message my-message">
                                                                    ${data.message}
                                                                    </div>
                                                                </li>`
            $(".chat-history").stop().animate({ scrollTop: $(".chat-history")[0].scrollHeight }, 1000);
        }
    }



}



document.querySelector('#message-to-send').focus();
document.querySelector('#message-to-send').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};




document.querySelector('#chat-message-submit').onclick = function (e) {
    const message_input = document.querySelector('#message-to-send');
    const message = message_input.value;
    userSocket.send(JSON.stringify({
        'message': message,
        'username': reciever_id
    }));
    console.log({
        'message': message,
        'username': reciever_id
    });
    message_input.value = '';
}


$("#chat-message-submit").click(function () {
    $(".chat-history").stop().animate({ scrollTop: $(".chat-history")[0].scrollHeight }, 1000);
});




function myFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}



function timeSince(date) {

    var seconds = Math.floor((new Date() - date) / 1000);

    var interval = seconds / 31536000;

    if (interval > 1) {
        return Math.floor(interval) + " years";
    }
    interval = seconds / 2592000;
    if (interval > 1) {
        return Math.floor(interval) + " months";
    }
    interval = seconds / 86400;
    if (interval > 1) {
        return Math.floor(interval) + " days";
    }
    interval = seconds / 3600;
    if (interval > 1) {
        return Math.floor(interval) + " hours";
    }
    interval = seconds / 60;
    if (interval > 1) {
        return Math.floor(interval) + " minutes";
    }
    return Math.floor(seconds) + " seconds";
}