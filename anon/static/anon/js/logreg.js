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

window.onclick = function(event) {
    if (event.target == document.getElementById('id-window-forgot')) {
        document.getElementById('id-window-forgot').style.display = "none";
        document.getElementById('email-forgot').value = '';
    }
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

dataOwnerButton.addEventListener('click', openRegistration);
dataProviderButton.addEventListener('click', openRegistration);

function openRegistration() {

    if(this.id === 'data-owner-button') {
        localStorage.setItem("typeAccount", 0);     // 0 => data owner
    } else {
        localStorage.setItem("typeAccount", 1);     // 1 => data provider
    }

}



//IMPLEMENT RESET PWD