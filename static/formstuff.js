
var light_settings = {
    'hue': 0,
    'sat': 0,
    'bri': 0,
    'on': false,
};

function createChangeListener(ws, field, value, parse_func) {
    let thing = document.getElementById(field);
    thing.addEventListener('input', function() {
        light_settings[field] = parse_func(this[value]);
        let msg = JSON.stringify(light_settings);
        ws.send(msg);
    });
}

function setLightValue(field, init_data) {
    document.getElementById(field).value = init_data[field];
}

window.onload = function() {
    let ws = new WebSocket(
        window.location.origin.replace('http', 'ws') + "/websocket");

    ws.onmessage = function(msg) {
        light_settings = JSON.parse(msg.data).init_vals;
        setLightValue('hue', light_settings);
        setLightValue('sat', light_settings);
        setLightValue('bri', light_settings);
        document.getElementById(field).checked = init_data['on'];
    };

    createChangeListener(ws, 'hue', 'value', parseInt);
    createChangeListener(ws, 'sat', 'value', parseInt);
    createChangeListener(ws, 'bri', 'value', parseInt);
    createChangeListener(ws, 'on', 'checked', function(bool) { return bool; });
};
