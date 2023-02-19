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

function ValidateEmail(input) {

    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

    if (input.value.match(validRegex))
        return true;
    else
        return false;

}

function onClickRegisterButton() {
    document.getElementById("email-hidden").value = document.getElementById("email-input").value;
    document.getElementById("pwd-hidden").value = password.value;
    document.getElementById("confirm-hidden").value = confirmPassword.value;
}

var specialKeys = new Array();
specialKeys.push(8);  //Backspace
specialKeys.push(9);  //Tab
specialKeys.push(46); //Delete
specialKeys.push(36); //Home
specialKeys.push(35); //End
specialKeys.push(37); //Left
specialKeys.push(39); //Right

function IsAlphaNumeric(e) {
    var keyCode = e.keyCode == 0 ? e.charCode : e.keyCode;
    console.log(e.keyCode)
    var ret = ((keyCode >= 33 && keyCode <= 43) || (keyCode >= 45 && keyCode <= 94) || (keyCode >= 96 && keyCode <= 122) || (specialKeys.indexOf(e.keyCode) != -1 && e.charCode != e.keyCode));
    return ret;
}

function IsAlphaNumericEmail(e) {
    var keyCode = e.keyCode == 0 ? e.charCode : e.keyCode;
    console.log(e.keyCode)
    var ret = ((keyCode >= 33 && keyCode <= 43) || (keyCode >= 45 && keyCode <= 122) || (specialKeys.indexOf(e.keyCode) != -1 && e.charCode != e.keyCode));
    return ret;
}

document.getElementById("reload-page").addEventListener('click', reloadPage);

function reloadPage() {
    document.location.reload();
}