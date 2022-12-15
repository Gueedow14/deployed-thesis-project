$( document ).ready(   
    function() {
        /* VARIABILI  */
        var nav = $(".menu_choice");
        var line = $(".line_menu");
        var attivo = $(".active");

        nav.find("ul li").on('click', 
            function() {

                var this_nav = $(this);

                line.animate(
                    {
                        left: this_nav.position().left,
                        width: this_nav.width() + 120
                    }

                );
                
                //togli classe active da tutti gli elementi li in ul nel nav
                nav.find("ul li").removeClass("active");

                //metti classe active sull'elemento selezionato
                if(!this_nav.hasClass("active")) {
                    this_nav.addClass("active");
                }
            }
        );

        // ON LOAD
        
        line.css(
            {
                width: attivo.width() + 120,
                left: attivo.position().left
            }
        );
    }
)


var password = document.getElementById('pwd-input');
var icon = document.getElementById('pwd-icon-eye');
var forgotPwd = document.getElementById('forgot-pwd');
var iconForgot = document.getElementById('button-close-forgot');
var loginMenu = document.getElementById('menu-login-option');
var registerMenu = document.getElementById('menu-register-option');
var loginContainer = document.getElementById('login-container');
var chkIcon = true;
var chkMenu = true;     //   true = Login ultimo ad avere focus;   false = Register ultimo ad avere focus;

password.addEventListener('keyup', logKeyPwd);
icon.addEventListener('click', onClickPwd);
forgotPwd.addEventListener('click', onClickForgot);
iconForgot.addEventListener('click', onClickIconForgot);
loginMenu.addEventListener('click', onClickLoginMenu);
registerMenu.addEventListener('click', onClickRegisterMenu);



function logKeyPwd(e) {
    if($('.pwd').val().length != 0)
        icon.style.opacity = "1";
    else {
        icon.style.opacity = "0";
        chkIcon = true;
        if($('#icona_pwd').hasClass("bi bi-eye-slash-fill")) {
            $('#icona_pwd').removeClass("bi bi-eye-slash-fill");
            $('#icona_pwd').addClass("bi bi-eye-fill");
        }
        password.setAttribute("type","password");
    }
}

function onClickPwd() {
    if(chkIcon) {
        $('#icona_pwd').removeClass("bi bi-eye-fill");
        $('#icona_pwd').addClass("bi bi-eye-slash-fill");
        password.setAttribute("type","text");
        chkIcon = false;
    } else {
        $('#icona_pwd').removeClass("bi bi-eye-slash-fill");
        $('#icona_pwd').addClass("bi bi-eye-fill");
        password.setAttribute("type","password");
        chkIcon = true;
    }
}

function onClickForgot() {
    document.getElementById('id-window-forgot').style.display = 'flex';
}

function onClickIconForgot() {
    document.getElementById('id-window-forgot').style.display = 'none';
    document.getElementById('email-forgot').value = '';
}

function onClickLoginMenu() {
    if(!chkMenu) {
        chkMenu = true;
        document.getElementById('login-container').style.display = "flex";
        document.getElementById('register-container').style.display = "none";
    }
}

function onClickRegisterMenu() {
    if(chkMenu) {
        chkMenu = false;
        document.getElementById('login-container').style.display = "none";
        document.getElementById('register-container').style.display = "block";
    }
}


const dataOwnerButton = document.getElementById('data-owner-button');
const dataProviderButton = document.getElementById('data-provider-button');
 

function validEmail(str) {
    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if(str.match(validRegex))
        return true;
    else
        return false;
}



const buttonForgotPwd = document.getElementById("button-forgot-pwd");

buttonForgotPwd.addEventListener('click', onButtonForgot)

function onButtonForgot() {
    if(document.getElementById("email-forgot").value.length === 0) {
        alert("Insert an E-Mail");
        return;
    } else if(!validEmail(document.getElementById("email-forgot").value)) {
        alert("Insert a valid E-Mail address");
        return;
    }
}

var loginButton = document.getElementById("login-button");

loginButton.addEventListener('click', onClickLogin);

function ValidateEmail(input) {

    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

    if (input.match(validRegex))
        return true;
    else
        return false;

}

function onClickLogin() {
    inputEmail = document.getElementById("email-input").value;
    inputPwd = password.value;

    if(inputEmail == "" && inputPwd == "") {
        alert("Remember to fill both fields.")
        return;
    }
    
    if(!ValidateEmail(inputEmail)) {
        alert("Insert a valid e-mail address.")
    }
}