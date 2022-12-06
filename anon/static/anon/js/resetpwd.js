const emailForgot = localStorage.getItem("email-forgot-pwd");



var password = document.getElementById('pwd-input');
var confirmPassword = document.getElementById('confirm-pwd-input');
var iconPwd = document.getElementById('pwd-icon-eye');
var iconConfirmPwd = document.getElementById('confirm-pwd-icon-eye');
var registerButton = document.getElementById('register-button');

var chkIcon = true;
var chkConfirmIcon = true;
 
password.addEventListener('keyup', logKeyPwd);
confirmPassword.addEventListener('keyup', logKeyConfirmPwd);
iconPwd.addEventListener('click', onClickPwd);
iconConfirmPwd.addEventListener('click', onClickConfirmPwd);
registerButton.addEventListener('click', onClickRegisterButton);


function logKeyPwd(e) {
    if($('#pwd-input').val().length != 0)
        iconPwd.style.opacity = "1";
    else {
        iconPwd.style.opacity = "0";
        chkIcon = true;
        if($('#icona-pwd').hasClass("bi bi-eye-slash-fill")) {
            $('#icona-pwd').removeClass("bi bi-eye-slash-fill");
            $('#icona-pwd').addClass("bi bi-eye-fill");
        }
        password.setAttribute("type","password");
    }
}

function logKeyConfirmPwd(e) {
    if($('#confirm-pwd-input').val().length != 0)
        iconConfirmPwd.style.opacity = "1";
    else {
        iconConfirmPwd.style.opacity = "0";
        chkConfirmIcon = true;
        if($('#confirm-icona-pwd').hasClass("bi bi-eye-slash-fill")) {
            $('#confirm-icona-pwd').removeClass("bi bi-eye-slash-fill");
            $('#confirm-icona-pwd').addClass("bi bi-eye-fill");
        }
        confirmPassword.setAttribute("type","password");
    }
}

function onClickPwd() {
    if(chkIcon) {
        $('#icona-pwd').removeClass("bi bi-eye-fill");
        $('#icona-pwd').addClass("bi bi-eye-slash-fill");
        password.setAttribute("type","text");
        chkIcon = false;
    } else {
        $('#icona-pwd').removeClass("bi bi-eye-slash-fill");
        $('#icona-pwd').addClass("bi bi-eye-fill");
        password.setAttribute("type","password");
        chkIcon = true;
    }
}

function onClickConfirmPwd() {
    if(chkConfirmIcon) {
        $('#confirm-icona-pwd').removeClass("bi bi-eye-fill");
        $('#confirm-icona-pwd').addClass("bi bi-eye-slash-fill");
        confirmPassword.setAttribute("type","text");
        chkConfirmIcon = false;
    } else {
        $('#confirm-icona-pwd').removeClass("bi bi-eye-slash-fill");
        $('#confirm-icona-pwd').addClass("bi bi-eye-fill");
        confirmPassword.setAttribute("type","password");
        chkConfirmIcon = true;
    }
}

function chkPwds(pwd, conf) {

    console.log("Pwd:" + pwd)
    console.log("Confirm:" + conf)
    

    if(pwd.length === 0 || conf.length === 0) {
        alert("Fill both password fields before continuing!")
    } else if(pwd != conf) {
        alert("The passwords don't match!")
    } else {
        return true
    }
    return false
}
 

function onClickRegisterButton() {
    if(chkPwds(document.getElementById("pwd-input").value, document.getElementById("confirm-pwd-input").value)) {
        //register modification in files
        location.href = "logreg";
    }
}

