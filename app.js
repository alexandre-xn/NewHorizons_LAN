const {
  app,
  BrowserWindow
} = require('electron')

let {
  PythonShell
} = require('python-shell')

const server_response_types = {
  SERVER_TIMEOUT: "Response : Server timeout",
  NO_HOSTS: "Response : No hosts",
  HOSTS_FOUND: "Response : Hosts found",
  SERVER_ERROR: "Response : Server error"
}
exports.server_response_types = server_response_types

let global_server_list = [
  ['switch.lan-play.com', 11452],
  ['lanplay.reboot.ms', 11451],
  ['open.t0g3pii.tk', 11451],
  ['frog-skins.com', 11451],
  ['chasehall.net', 11451],
  ['nook-inc.net', 11451],
  ['81.98.26.94', 11451],
  ['lanplay2.reboot.ms', 11451],
  ['joinsg.net', 11451],
  ['switch.jayseateam.nl', 11451],
  ['nook-hq.ml', 11451],
  ['nxlan-w.dentora.ca', 11451] 
]

function createWindow() {
  let win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  })
  win.setFullScreen(true)

  //win.setMenu(null)
  win.loadFile('index.html')

  query_all_servers(win, global_server_list)
}

async function query_all_servers(win, server_list) {
  for (var i = 0; i < server_list.length; i++) {
    query_server({
      args: server_list[i]
    }, win)
  }
}

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

async function query_server(options, window) {
  PythonShell.run('main.py', options, async function (err, results) {
    if (err) {
      console.log(err)
      results = [options.args[0] + ":" + options.args[1], options.args[0] + ":" + options.args[1], server_response_types.SERVER_ERROR, '[]']
    }
    window.webContents.send('server-data', results)
    await sleep(3000)
    query_server(options, window)
  });
}

app.whenReady().then(createWindow)