
var light_settings = {
    'hue': 0,
    'sat': 0,
    'bri': 0,
};

function createChangeListener(ws, field) {
    let thing = document.getElementById(field);
    thing.addEventListener('input', function() {
        light_settings[field] = parseInt(this.value);
        let msg = JSON.stringify(light_settings);
        console.log(msg);
        ws.send(msg);
    });
}

function setLightValue(field, init_data) {
    console.log(init_data[field]);
    document.getElementById(field).value = init_data[field];
}

window.onload = function() {
    console.log(window.location);
    let ws = new WebSocket(
        window.location.origin.replace('http', 'ws') + "/websocket");

    ws.onmessage = function(msg) {
        light_settings = JSON.parse(msg.data).init_vals;
        console.log(light_settings);
        setLightValue('hue', light_settings);
        setLightValue('sat', light_settings);
        setLightValue('bri', light_settings);
    };

    createChangeListener(ws, 'hue');
    createChangeListener(ws, 'sat');
    createChangeListener(ws, 'bri');
};
