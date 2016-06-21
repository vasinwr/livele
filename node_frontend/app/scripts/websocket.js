(function(){
  console.log('websocket.js used');
  var socket = new WebSocket('ws://127.0.0.1:8000/all/');
  socket.onmessage = function(message){
    var data = JSON.parse(message.data);
    if(data.green_bar || data.red_bar){
      document.getElementById('red_bar').style.width = data.red_bar + '%';
      document.getElementById('green_bar').style.width = data.green_bar + '%';
    }
  }

})();
