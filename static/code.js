var info_bar_event_source = new EventSource("/info_bar");
info_bar_event_source.onmessage = function(event) { document.getElementById("info_bar").innerHTML = event.data; };


const xhr = new XMLHttpRequest();

const change_mode_button_find_target = document.getElementById("change_mode_button_find_target");
const change_mode_button_get_distance = document.getElementById("change_mode_button_get_distance");
const change_mode_button_use_compass = document.getElementById("change_mode_button_use_compass");

change_mode_button_find_target.addEventListener("click", () => change_mode("find_target"));
change_mode_button_get_distance.addEventListener("click", () => change_mode("get_distance"));
change_mode_button_use_compass.addEventListener("click", () => change_mode("use_compass"));

change_mode_button_find_target.style.backgroundColor = "lightblue";

function change_mode(mode) {
    change_mode_button_find_target.style.backgroundColor = mode === "find_target" ? "lightblue" : "white";
    change_mode_button_get_distance.style.backgroundColor = mode === "get_distance" ? "lightblue" : "white";
    change_mode_button_use_compass.style.backgroundColor = mode === "use_compass" ? "lightblue" : "white";

    xhr.open("POST", "/change_mode", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ "mode": mode }));
}