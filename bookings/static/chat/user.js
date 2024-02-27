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


function toDataURL(file, callback) {
    var reader = new FileReader();
    reader.onload = function () {
        var dataURL = reader.result;
        callback(dataURL);
    }
    reader.readAsDataURL(file);
}

document.getElementById('chatUploadedFile').addEventListener('change', async function(event){
    var file = event.target.files[0];
    const base64 = await convertBase64(file);
    localStorage.setItem("userUploadedFile" , base64);
    var userId = $('#chatWithDesigner').val();
    toDataURL(file, function(dataURL){
        userSocket.send(JSON.stringify({
        'type' : 'file',
        'fileName':file.name, 
        'dataURL': dataURL,
        'username' : userId,
        "message" : ""
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

function uploadChatFile(){
    document.getElementById("chatUploadedFile").click();
    
}


$("#chat_icon").click(function () {
    $("#chat_box").toggle('.show')
    $(".chat-content").animate({ scrollTop: $('.chat-content').height() }, 1000);
    $(".chat-content").scroll(0);

    var orderId = $('#chatOrderID').val();
    var userId = $('#chatUserID').val();
    var designerId = $('#chatWithDesigner').val();

    var reciever_id = designerId;
    // getChatMessages(userId, designerName, orderId);
    var sockerUrl = getChatSocketUrl(reciever_id)
    if(userSocket == undefined){
        userSocket = createSocket(sockerUrl);
    }
    userSocket.onopen = function (e) {
        //console.log("CONNECTION ESTABLISHED", sockerUrl);
    }
    userSocket.onclose = function (e) {
        //console.log("CONNECTION LOST", sockerUrl);
    }
    userSocket.onerror = function (e) {
        //console.log("ERROR OCCURED", sockerUrl);
    }

    console.log("Sender", userId)
    console.log("RecieverId", reciever_id)
    userSocket.onmessage = function (e) {
        //console.log(e.data.message)
        const data = JSON.parse(e.data);
        var today = new Date();
        time_since = timeSince(today);
        var file = localStorage.getItem("userUploadedFile");
        if (data.user_id == reciever_id) {
            //To check the input is URL
            var pattern = /^(http|https)?:\/\/[a-zA-Z0-9-\.]+\.[a-z]{2,4}/;
            let senderHTML = '';
            if(pattern.test(data.message)){
                senderHTML = `
                <div class="sender-text"> ${'<a href=' + data.message+ ' class="sender-link" target="_blank">' + data.message + '</a>'}</div>
            `
            }else if(file && !data.message){
                document.querySelector('#chat-body').innerHTML +=
                    `
                <div class="sender-text" style="width: 50%;">${'<div class="sender_img"><img src='+file+'><a download="File1.png" href='+file+'><img src="../../static/img/icons-download.png" class="download-icon"></a>'}</div>
    
                `
            }
            else {
                senderHTML = `
                <div class="sender-text"> ${data.message}</div>
            `
            }
            document.querySelector('#chat-body').innerHTML += senderHTML
        } else if(data.message){
            document.querySelector('#chat-body').innerHTML += `
            <div class="reciever-text"> ${data.message}</div>
        `
                
        } 
        else if(file && !data.message){
            document.querySelector('#chat-body').innerHTML +=
                    `
                <div class="reciever-text" style="width: 50%;">${'<div class="sender_img"><img src=/media/chat_uploads/'+data.file_name+'><a download="File1.png" href='+data.file_name+'><img src="../../static/img/icons-download.png" class="download-icon"></a>'}</div>
    
                `
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
        //console.log("This is the message", message_input.value);
        if(userSocket.readyState == userSocket.CLOSED){
            connectToSocket(reciever_id);
        } 
        userSocket.send(JSON.stringify({
            'message': message,
            'username': reciever_id
        }));
        // console.log({
        //     'message': message,
        //     'username': reciever_id
        // });
        message_input.value = '';
    }


    // $("#chat-message-submit").click(function () {
    //     $(".chat-history").stop().animate({ scrollTop: $(".chat-history")[0].scrollHeight }, 1000);
    // });

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


        
    
});
