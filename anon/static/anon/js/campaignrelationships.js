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

document.getElementById("reload-page").addEventListener('click', reloadPage);

function reloadPage() {
    document.location.reload();
}