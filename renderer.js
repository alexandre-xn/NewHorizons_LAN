const server_response_types = {
    SERVER_TIMEOUT: "Response : Server timeout",
    NO_HOSTS: "Response : No hosts",
    HOSTS_FOUND: "Response : Hosts found",
    SERVER_ERROR: "Response : Server error"
}

ipc = require('electron').ipcRenderer;

var last_server_status = {}

ipc.on('server-data', (_event, message) => {
    var server_id = message[0]
    var server_slot = document.getElementById(server_id)
    var server_response = message[2]

    var server_status = get_text_to_display(message)

    if (server_slot) {
        if (server_response != server_response_types.SERVER_TIMEOUT) {
            if (!(server_response != server_response_types.HOSTS_FOUND && last_server_status[server_id] == server_response_types.HOSTS_FOUND)) {
                server_slot.textContent = server_status
                last_server_status[server_id] = server_response
            }
        }
    } else {
        var tag = document.createElement("li")
        tag.innerHTML = ""
        tag.appendChild(document.createTextNode(server_status))
        tag.id = server_id
        var connect_btn = document.createElement("button")
        /*connect_btn.innerHTML = '<button type="button" class="button">Connect</button>'
        tag.appendChild(connect_btn)*/
        last_server_status[server_id] = server_response
        document.querySelector("#test").appendChild(tag)
    }
})

function get_islands(host_list) {
    var islands = [],
        pos = host_list.indexOf("('")

    while (~pos) {
        var current_island = " | 🏝️ " + host_list.substring(pos + 2, host_list.indexOf("',", pos))
        if(!islands.includes(current_island)) {
            islands.push(current_island)
        }
        pos = host_list.indexOf("('", pos + 1)
    }
    return islands
}

function get_text_to_display(message) {
    var resp_field = message[2]
    switch (resp_field) {
        case server_response_types.SERVER_TIMEOUT:
            return message.slice(1, 2) + " : ⏱️ Server timed out"
        case server_response_types.NO_HOSTS:
            return message.slice(1, 2) + " : ❌ No islands available"
        case server_response_types.HOSTS_FOUND:
            return message.slice(1, 2) + get_islands(message[3])
        default:
            return message.slice(1, 2) + " : 🛑 Error with server data"
    }
}

/*sendMessageButton.addEventListener('click', event => {
    ipc.send('reply', `Send message from second window to renderer via main.`);
    window.close();
});*/