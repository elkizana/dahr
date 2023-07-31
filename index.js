
const { app, BrowserWindow,ipcMain  } = require('electron');

const {shell} = require('electron');
 
const Store = require('electron-store');

const store = new Store()












process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';
function createWindow() {
  const win = new BrowserWindow({
   /*  width: 600,
    height: 400, */
    frame: false,
    transparent: true, 
    //resizable : false ,

    icon : "",
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true,
      contextIsolation: false
    } 
  })  

  win.loadFile('main.html')
  //win.maximize()
  win.setMenuBarVisibility(false)
  //win.webContents.openDevTools()
}
app.setName("الخزانة")
app.commandLine.appendSwitch('enable-experimental-web-platform-features');

app.whenReady().then(createWindow)


app.on('window-all-closed', () => {



  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {

  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }

})

ipcMain.on('saveInputValue', (event, inputObj) => {
  
  store.set('inputValues', inputObj)

});

ipcMain.on('getSavedInputValue', (event) => {
  const savedInputObj = store.get('inputValues');
  event.sender.send('sendSavedInputValue', savedInputObj);
});
