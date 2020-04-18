const server_response_types = {
    TIMED_OUT: 'Response : Timed out (no hosts ?)',
    NORMAL: ''
}

ipc = require('electron').ipcRenderer;
ipc.on('server-data', (event, message) => {
    console.log(message)
    var server_card = document.getElementById(message[0])
    var server_status = ""
    message[3].split(",")
    console.log(message[3])
    if (message[3] == '[]' && message[2] != server_response_types.TIMED_OUT) {
        server_status = message.slice(1, 2) + " | ❌ No hosts available"
    } else if (message[3] != '[]') {
        islands = get_islands_names(message[3])
        server_status = message.slice(1, 2) + islands
    } else {
        server_status = message.slice(1, 2) + " | ⏱️ Server timed out"
    }
    if (server_card) {
        server_card.textContent = server_status
    } else {
        var tag = document.createElement("div")
        tag.appendChild(document.createTextNode(server_status))
        tag.id = message[0]
        document.querySelector("#test").appendChild(tag)
    }
})

function get_islands_names(m) {
    /*var islands = ""
    islands += " | 🏝️ " + m.substr(m.indexOf("'") + 1, m.indexOf("',") - 3)
    return islands*/
    return " | 🏝️ " + m
}

sendMessageButton.addEventListener('click', event => {
    ipc.send('reply', `Send message from second window to renderer via main.`);
    window.close();
});