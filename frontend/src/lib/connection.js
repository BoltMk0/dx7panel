import { writable, get } from "svelte/store";
import { getModel } from "./model"
import { MESSAGE_ID } from "./const.js";

const WS_PORT = 5000;


var _connectionTimeout;

class Connection {
    _connect_started = false;
    _msg_enable = true;
    connected = writable(0)
    socket;

    get_host(){
        let to_ret = localStorage.getItem('dx7panel-host');
        if(to_ret === null){
            to_ret = `${window.location.hostname}:${WS_PORT}`;
        }
        return to_ret;
    }

    set_host(new_host){
        localStorage.setItem('dx7panel-host', new_host);
    }

    connect() {
        clearInterval(this._connectionTimeout);
        if(this.socket) this.socket.close();
        this.connected.set(1);
        const serverurl = "ws://" + this.get_host();
        console.log("Connecting to ", serverurl);
        this.socket = new WebSocket(serverurl);
        this.socket.onopen = (ev) => {
            console.log("Connected!");
            clearTimeout(_connectionTimeout)
            this.connected.set(2);
            this.send(JSON.stringify([MESSAGE_ID.SUBSCRIBE]));
            this.send(JSON.stringify([MESSAGE_ID.VOICE_DUMP]));
            this.send(JSON.stringify([MESSAGE_ID.GET_SETTINGS]));
            this.send(JSON.stringify([MESSAGE_ID.BANK_DUMP]));
        }

        this.socket.onclose = (ev) => {
            this.connected.set(0);
            this.socket = null;
            this._connect_started = false;
            _connectionTimeout = setTimeout(() => {
                this.connect();
            }, 1000);
            console.log("Socket closed. Reconnecting in 1s...");
        }

        this.socket.onerror = (ev) => {
            this.connected.set(0);
            this.socket = null;
            console.log("Socket error");
        }

        this.socket.addEventListener('message', (msg) => {
            let msgobj = JSON.parse(msg.data);
            this._msg_enable = false;
            try {
                getModel().update(msgobj);
            } finally {
                this._msg_enable = true;
            }
        });
    }

    send(msg) {
        if(typeof msg !== 'string') msg = JSON.stringify(msg);
        if (this._msg_enable && this.socket && get(this.connected) == 2){
            this.socket.send(msg);
        }
    }
}

var _connection;

function getConnection() {
    if (!_connection) {
        console.log("Creating new connection");
        _connection = new Connection();
    }
    return _connection;
}

export { getConnection, WS_PORT }