async function load_name(){
    return await fetch('/get_name')
         .then(async function (response) {
            return await response.json();
        }).then(function (text) {
            return text["name"]
        });
};

async function load_messages() {
    return await fetch('/get_messages')
     .then(async function (response) {
        return await response.json();
    }).then(function (text) {
        console.log(text)
        return text
    });
}

var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on( 'connect', function() {
    socket.emit( 'event', {
      data: 'User Connected'
    } )
    var form = $( 'form#msgForm' ).on( 'submit', async function( e ) {
      e.preventDefault()

      // get input from message box
      let msg_input = document.getElementById("msg")
      let user_input = msg_input.value
      let user_name = await load_name()

      // clear msg box value
      msg_input.value = ""

      // send message to other users
      socket.emit( 'event', {
        message : user_input,
        name: user_name
      } )
    } )
  } )
  socket.on( 'message response', function( msg ) {
    add_messages(msg)
  })

window.onload = async function() {
    var msgs = await load_messages()
    for (msg of msgs){
        add_messages(msg)
    }
}

async function add_messages(msg){
    if( typeof msg.name !== 'undefined' ) {
            var arr = " yyyy-mm-dd hh:mm:ss".split(/-|\s|:/);// split string and create array.
            var date = new Date(arr[0], arr[1] -1, arr[2], arr[3], arr[4], arr[5]);

            if ( typeof msg.time !== "undefined") {
                var n = msg.time
            }else{
                var n = date
            }
            var global_name = await load_name()

            var content = '<div class="container">' + '<b style="color:#000" class="right">'+msg.name+'</b><p>' + msg.message +'</p><span class="time-right">' + n + '</span></div>'
            if (global_name == msg.name){
                content = '<div class="container darker">' + '<b style="color:#000" class="left">'+msg.name+'</b><p>' + msg.message +'</p><span class="time-left">' + n + '</span></div>'
            }
            // update div
            var messageDiv = document.getElementById("messages")
            messageDiv.innerHTML += content
    }
}
