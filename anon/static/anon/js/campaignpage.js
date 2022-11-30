var titleName = document.getElementById("campaign-name-title");
var headerName = document.getElementById("campaign-name-header");

var img = document.getElementById("img-div");

img.addEventListener('mousemove', zoom)


function zoom(e) {
    var zoomer = e.currentTarget;
    e.offsetX ? (offsetX = e.offsetX) : (offsetX = e.touches[0].pageX);
    e.offsetY ? (offsetY = e.offsetY) : (offsetX = e.touches[0].pageX);
    x = (offsetX / zoomer.offsetWidth) * 100;
    y = (offsetY / zoomer.offsetHeight) * 100;
    zoomer.style.backgroundPosition = x + "% " + y + "%";
}
  


var infoButton = document.getElementById("info-button");
var infoWindow = document.getElementById("info-window");
var infoClose = document.getElementById("info-close");

infoButton.addEventListener('click', openInfoWindow);
infoClose.addEventListener('click', closeInfoWindow);


function openInfoWindow() {
    infoWindow.style.display = "block";
}

function closeInfoWindow() {
    infoWindow.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == infoWindow)
        infoWindow.style.display = "none";
}



const compareButton = document.getElementById('compare-button');

compareButton.addEventListener('click', compareCampaign);

function compareCampaign() {
    //data to be passed

    location.href = "comparehome";
}


const anonButton = document.getElementById('anon-button');

anonButton.addEventListener('click', anonCampaign);

function anonCampaign() {
    //data to be passed

    location.href = "anonymize";
}