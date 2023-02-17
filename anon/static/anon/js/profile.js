var chkPwd = false;     //false: pwd not visible

const pwd = document.getElementById("pwd");
const pwdIconDivSee = document.getElementById("pwd-icon-div-see");
const pwdIconSee = document.getElementById("pwd-icon-see");

pwdIconDivSee.addEventListener('click', changeVisibility);

function changeVisibility() {
    if(chkPwd) {
        pwdIconSee.classList.remove("bi-eye-slash-fill");
        pwdIconSee.classList.add("bi-eye-fill");
        pwd.setAttribute("type","password");
        chkPwd = false;
    } else {
        pwdIconSee.classList.remove("bi-eye-fill");
        pwdIconSee.classList.add("bi-eye-slash-fill");
        pwd.setAttribute("type","text");
        chkPwd = true;
    }
}

const windowChangePwd = document.getElementById("id-window-change");

const pwdIconDivChange = document.getElementById("pwd-icon-div-change");
const pwdIconChange = document.getElementById("pwd-icon-change");

const iconClose = document.getElementById("button-close");

pwdIconDivChange.addEventListener('click', openWindow);
iconClose.addEventListener('click', closeWindow);


function openWindow() {
    windowChangePwd.style.display = "flex";
}

function closeWindow() {
    windowChangePwd.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == windowChangePwd)
        closeWindow();
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