document.getElementById("kg-button").addEventListener('click', onClickShow);
document.getElementById("close-button").addEventListener('click', onClickClose);

function onClickShow() {
    document.getElementById('kg-window').style.display = 'flex';
}

function onClickClose() {
    document.getElementById('kg-window').style.display = 'none';
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

document.getElementById("button-close-logout").addEventListener('click', onClickCloseLogout)

function onClickCloseLogout() {
  document.getElementById("window-logout").style.display = "none"
}