
var light_settings = {
    'hue': 0,
    'sat': 0,
    'bri': 0,
};

window.onload = function() {
    function createChangeListener(field) {
        let thing = document.getElementById(field);
        thing.addEventListener('input', function() {
            light_settings[field] = parseInt(this.value);
            let msg = JSON.stringify(light_settings);
            console.log(msg);
            ws.send(msg);
        });
    }

    let ws = new WebSocket("ws://localhost:8080/websocket");

    ws.onopen = () => function() {
        ws.send("ohai");
    };

    createChangeListener('hue');
    createChangeListener('sat');
    createChangeListener('bri');
};
