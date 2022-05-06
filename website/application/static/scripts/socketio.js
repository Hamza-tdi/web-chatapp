document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://'+document.domain+':'+location.port);
    socket.on('connect', () => {
        console.log('I am connected')
    });

    socket.on('message', data => {
        const p = document.createElement('p')
        const span = document.createElement('span')
        const br = document.createElement('br')
        span.innerHTML = data.username
        p.innerHTML = data.username + br.outerHTML + data.msg
        document.querySelector('#display-message-section').append(p)
    });

    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user-message').value, 'username': username});
        console.log(document.querySelector('#user-message').value);
        document.querySelector('#user-message').innerHTML = ''
    }
})