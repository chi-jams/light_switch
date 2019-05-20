
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

    console.log(window.location);
    let ws = new WebSocket(
        window.location.origin.replace('http', 'ws') + "/websocket");

    ws.onopen = () => function() {
        ws.send("ohai");
    };

    createChangeListener('hue');
    createChangeListener('sat');
    createChangeListener('bri');
};
