const net = require('net');
const path = 'socket.sock';

class Client {
    constructor(path, timeout) {
        this.socket = net.createConnection(path)
        this.socket.settimeout(timeout)
        this.socket.on("connect", () => {
            console.log("Succesfully connected!!");
        });
        this.socket.on("data", (data) => {
            console.log('Recieved data: ') + data.toString();
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
}