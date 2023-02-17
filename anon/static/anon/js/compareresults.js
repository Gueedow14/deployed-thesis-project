var tableBox = document.getElementById("tableBox");
var table = document.getElementById("myTable");


var chartBox = document.getElementById("chartBox");
var chart = document.getElementById("myChart");







var toggleButton = document.getElementById('toggle-button');

toggleButton.addEventListener('click', onClickToggle);

async function onClickToggle() {

    if(this.checked) {

        chartBox.style.animation = "chartOutAnim .7s ease 1";
        chartBox.style.display = "none";
        tableBox.style.display = "flex";
        tableBox.style.animation = "tableInAnim .7s ease 1";

    } else {

        tableBox.style.animation = "tableOutAnim .7s ease 1";
        tableBox.style.display = "none";
        chartBox.style.display = "block";
        chartBox.style.animation = "chartInAnim .7s ease 1";

    }

}




const finishButton = document.getElementById('finish-button');

finishButton.addEventListener('click', closeResults);

function closeResults() {
    
}


document.getElementById("menu-button").addEventListener('click', onClickMenu);

chkOpen = false;

function onClickMenu() {
    if(chkOpen) {
        $("#menu-options").slideUp(300);
        chkOpen = false;
    } else {
        $("#menu-options").slideDown(300);
        chkOpen = true;
    }
}

document.getElementById("logout-button").addEventListener('click', onClickLogout)

function onClickLogout() {
  document.getElementById("window-logout").style.display = "flex"
}

document.getElementById("button-close").addEventListener('click', onClickClose)

function onClickClose() {
  document.getElementById("window-logout").style.display = "none"
}
