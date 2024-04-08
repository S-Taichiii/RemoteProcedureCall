const net = require('net');
const fs = require("fs");

class Client {
    constructor(path, timeout=60) {
        this.socket = null;
        this.path = path;
        this.timeout = timeout;
        
        this.connect();

        const jsonFilePath = "input.json";
        this.send(jsonFilePath);
    };
    
    connect(){
        this.socket = net.createConnection(this.path)
        this.socket.setTimeout(this.timeout)
        this.socket.on("connect", () => {
            console.log("Succesfully connected!!");
        });
        this.socket.on("data", (data) => {
            console.log('Result data: ' + data.toString());
        });
        this.socket.on('end', () => {
            console.log('Closing current connection!!');
        });
        this.socket.on('timeout', () => {
            console.log('timed out!');
            this.socket.destroy();
        });
        this.socket.on('error', (error) => {
            console.log(error.message);
        });
    }
    
    send(file) {
        fs.readFile(file, 'utf-8', (err, data) => {
            if (err) {
                console.error('ファイルを読み込めませんでした。', err);
                return;
            }
            
            console.log(data)

            try {
                this.socket.write(data);
            } catch (error) {
                console.error('JSONデータをパースできませんでした。', error);
            }
        })
    }
}

const path = '/tmp/socket.sock';
client = new Client(path, 60);