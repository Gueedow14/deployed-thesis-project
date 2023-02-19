var invalidRemovalButton = document.getElementById('sr-button');
var msAlgButton = document.getElementById('ms-button');


var yesButton = document.getElementById("yes-button");
var noButton = document.getElementById("no-button");

const radioButtons = document.getElementsByClassName("radio_alg");

for(var i = 0 ; i < radioButtons.length ; i++) {
    radioButtons[i].addEventListener('click', onClickRadio)
}

selectedRadio = null;


invalidRemovalButton.addEventListener('click', onClickValidationButton);
invalidRemovalButton.classList.remove('disabled_button');
invalidRemovalButton.classList.add('button');
msAlgButton.addEventListener('click', onClickValidationButton);
msAlgButton.classList.remove('disabled_button');
msAlgButton.classList.add('button');


var validationOpen = false;

function onClickValidationButton() {

    if(this.id == "sr-button") {
        invalidRemovalButton.classList.remove("button")
        invalidRemovalButton.classList.add("selected_button")
        msAlgButton.classList.remove("selected_button")
        msAlgButton.classList.add("button")
    } else if(this.id == "ms-button") {
        msAlgButton.classList.remove("button")
        msAlgButton.classList.add("selected_button")
        invalidRemovalButton.classList.remove("selected_button")
        invalidRemovalButton.classList.add("button")
    }

    yesButton.addEventListener('click', onClickDownloadButton);
    yesButton.classList.remove('disabled_button');
    yesButton.classList.add('button');
    noButton.addEventListener('click', onClickDownloadButton);
    noButton.classList.remove('disabled_button');
    noButton.classList.add('button');
    
    document.getElementById("selected-valid").value = this.id.split("-")[0];

}


function onClickDownloadButton() {

    if(this.id == "yes-button") {
        yesButton.classList.remove("button")
        yesButton.classList.add("selected_button")
        noButton.classList.remove("selected_button")
        noButton.classList.add("button")
    } else if(this.id == "no-button") {
        noButton.classList.remove("button")
        noButton.classList.add("selected_button")
        yesButton.classList.remove("selected_button")
        yesButton.classList.add("button")
    }

    document.getElementById("anonymize-button-container").style.display = "flex"

    document.getElementById("selected-save").value = this.id.split("-")[0];

}


document.getElementById("anon-button").addEventListener('click', showLoader)

function showLoader() {
    document.getElementById("loader-div").style.display = "flex";
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

document.getElementById("reload-page").addEventListener('click', reloadPage);

function reloadPage() {
    document.location.reload();
}