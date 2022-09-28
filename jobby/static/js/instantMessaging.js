function getRecipient(r, callback){
  const request = new XMLHttpRequest();
  var url = '/get-recipient/' + r;
  request.open('GET', url);
  var username;

  request.onload = () =>{
    if (request.status == 200){
      username = JSON.parse(request.responseText);
      if(callback) callback(username);
    }
  }
  request.send();
}

document.addEventListener('DOMContentLoaded', () => {
  var persons = document.getElementsByName('persons');
  var parent = document.getElementById('parent');
  var messageArea = document.getElementById('messageArea');
  var sendMsg = document.getElementById('sendMsg');
  var person_id;
  var imgSrcSender;
  var imgSrcReciever;

  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('connect', () =>{
    msg = document.getElementsByName('sendMessage');
    msg.forEach(function(m){
      m.onclick = () => {
        var msgResult = document.getElementById('msgResult');
        var formData = document.getElementById('formData');
        err = document.getElementById('errorBody');
        var recipient_id = parseInt(m.getAttribute('data'));
        getRecipient(recipient_id, function(username){
          if (formData.style.display == 'none'){
            formData.style.display = "block";
            msgResult.style.color = "black"
            formData.firstElementChild.value = ""
          }
          msgResult.innerText = "Send Message to " + username.username;
        })
        document.getElementById('sendButton').onclick = () =>{
          body = document.getElementById('body').value;
          if(body != ""){
            socket.emit("send message", {"to": recipient_id, "body": body})
          }
          else{
            err.innerText = "* You didn't write anything";
            err.style.color = "red";
          }
        }
      }
    })
  })

  socket.on('message success', data => {
    if(data.success){
      formData.style.display = "none";
      msgResult.innerText = "Message has been sent!";
      msgResult.style.color = "green";
      err.style.display = "none";
    }
  })

  persons.forEach(function(p){
    p.onclick = () =>{
      //remove all active class before assigning active class
      persons.forEach(function(p){
        p.removeAttribute('class');
        p.style.backgroundColor = "white";
      })

      parent.innerHTML = "";
      p.setAttribute('class', 'active-message')
      p.style.backgroundColor = "#ececec";
      person_id = parseInt(p.getAttribute('data'));

      const request = new XMLHttpRequest();
      var url = '/get-all-message/' + person_id;
      request.open('GET', url);

      request.onload = () =>{
        if (request.status == 200){
          response = JSON.parse(request.responseText);
          imgSrcSender = response.imgSrcSender;
          imgSrcReciever = response.imgSrcReciever;
          document.getElementById('recipient_name').innerText = response.recipient_name;

          response.payload.forEach(function(item){
            if(response.currentUserId == item[2]){
              createMsgField(parent, item, 'message-bubble me', imgSrcSender);
            }
            else{
              createMsgField(parent, item, 'message-bubble', imgSrcReciever);
            }
          })
        }
      }
      request.send();
    }

  })

  sendMsg.disabled = true;
  sendMsg.style.color = "red";
  sendMsg.style.border = "1px solid red";
  sendMsg.style.backgroundColor = "white";

  messageArea.addEventListener('input', function(e){
    if(messageArea.value.length > 0 && person_id != null){
      sendMsg.disabled = false;
      sendMsg.style.backgroundColor = "blue";
      sendMsg.style.color = "white";
      sendMsg.style.border = "";
    }
    else{
      sendMsg.disabled = true;
      sendMsg.style.backgroundColor = "white";
      sendMsg.style.color = "red";
      sendMsg.style.border = "1px solid red"
    }
  })

  messageArea.addEventListener('keydown', function(e){
    if(e.keyCode == 13){
      sendMsg.click();
      e.preventDefault();
    }
  })

  // while(true){
  //   if(messageArea.value.length > 0){
  //
  //   }
  //   else{
  //
  //   }
  //
  //   messageArea.addEventListener('input', function _writing(){
  //     console.log("input event fired");
  //     messageArea.removeEventListener('input', _writing)
  //     //socket.emit("start writing", {'recipient_id': person_id})
  //   })
  // }


  // socket.on("put writing field", data =>{
  //   // console.log("all the way here");
  //   // console.log(data);
  //   // typingDiv = document.createElement('div');
  //   // typingDiv.setAttribute('class', 'typing-indicator');
  //   // span = document.createElement('span');
  //   // typingDiv.appendChild(span);
  //   // console.log("sender_id", data.sender_id);
  //   // console.log("person_id", person_id)
  //   if(data.sender_id == person_id){
  //     createMsgField(parent, ["..."], 'typing-indicator');
  //   }
  //   //console.log(typingDiv);
  // })

  sendMsg.onclick = () =>{
    socket.emit('private message', {'msg': messageArea.value, 'recipient': person_id})
    createMsgField(parent, [messageArea.value], 'message-bubble me', imgSrcSender);
    sendMsg.disabled = true;
    sendMsg.style.color = "red";
    sendMsg.style.border = "1px solid red";
    sendMsg.style.backgroundColor = "white";
    messageArea.value = "";
  }

  socket.on('message sent back', data =>{
    if(data.sender_id == person_id){
      createMsgField(parent, [data.prv], 'message-bubble', imgSrcReciever);
    }
  })

})

function createMsgField(parent, item, className, imgSrc){
  msg = document.createElement('div');
  msg.setAttribute('class', className);
  msgInner = document.createElement('div');
  msgInner.setAttribute('class', 'message-bubble-inner')
  msgAvatar = document.createElement('div');
  msgAvatar.setAttribute('class', 'message-avatar')
  img = document.createElement('img');
  img.src = "/static/images/" + imgSrc
  msgText = document.createElement('div');
  msgText.setAttribute('class', 'message-text')
  p = document.createElement('p');
  clearfix = document.createElement('div');
  clearfix.setAttribute('class', 'clearfix')
  p.innerText = item[0];
  msgAvatar.appendChild(img);
  msgText.appendChild(p);
  msgInner.appendChild(msgAvatar);
  msgInner.appendChild(msgText);
  msg.appendChild(msgInner);
  msg.appendChild(clearfix);
  parent.appendChild(msg);
  parent.scrollTop = parent.scrollHeight-parent.clientHeight;
}
