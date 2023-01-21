document.getElementById("anonymize-button-container").style.display = "none";


var hdbscanButton = document.getElementById('hdbscan-button');
var kMedoidsButton = document.getElementById('km-button');
var vacButton = document.getElementById('vac-button');

hdbscanButton.addEventListener('click', onClickClusteringButton);
kMedoidsButton.addEventListener('click', onClickClusteringButton);
vacButton.addEventListener('click', onClickClusteringButton);



var invalidRemovalButton = document.getElementById('sr-button');
var msAlgButton = document.getElementById('ms-button');


var yesButton = document.getElementById("yes-button");
var noButton = document.getElementById("no-button");



const radioButtons = document.getElementsByClassName("radio_alg");

for(var i = 0 ; i < radioButtons.length ; i++) {
    radioButtons[i].addEventListener('click', onClickRadio)
}

selectedRadio = null;

function onClickClusteringButton() {

    if(this.id == "hdbscan-button") {
        $("#hdbscan-options").slideDown(300);
        $("#km-options").slideUp(300);
    } else if(this.id == "km-button") {
        $("#km-options").slideDown(300);
        $("#hdbscan-options").slideUp(300);
    } else {
        $("#hdbscan-options").slideUp(300);
        $("#km-options").slideUp(300);
        if(vacButton.classList.contains("button")) {
            vacButton.classList.remove("button")
            vacButton.classList.add("selected_button")
        }

        if(hdbscanButton.classList.contains("selected_button")) {
            hdbscanButton.classList.remove("selected_button")
            hdbscanButton.classList.add("button")
        }

        if(kMedoidsButton.classList.contains("selected_button")) {
            kMedoidsButton.classList.remove("selected_button")
            kMedoidsButton.classList.add("button")
        }

        invalidRemovalButton.addEventListener('click', onClickValidationButton);
        invalidRemovalButton.classList.remove('disabled_button');
        invalidRemovalButton.classList.add('button');
        msAlgButton.addEventListener('click', onClickValidationButton);
        msAlgButton.classList.remove('disabled_button');
        msAlgButton.classList.add('button');

        document.getElementById("selected-clust").value = this.id.split("-")[0];

        if(selectedRadio != null) {
            selectedRadio.checked = false;
            selectedRadio = null;
        }
    }

}


function onClickRadio() {
    selectedRadio = this

    if(vacButton.classList.contains("selected_button")) {
        vacButton.classList.remove("selected_button")
        vacButton.classList.add("button")
    }

    if(this.id.split("-")[0] == "hdbscan") {
        if(kMedoidsButton.classList.contains("selected_button")) {
            kMedoidsButton.classList.remove("selected_button")
            kMedoidsButton.classList.add("button")
        }
        
        if(!hdbscanButton.classList.contains("selected_button")) {
            hdbscanButton.classList.remove("button")
            hdbscanButton.classList.add("selected_button")
        }
    } else {
        if(hdbscanButton.classList.contains("selected_button")) {
            hdbscanButton.classList.remove("selected_button")
            hdbscanButton.classList.add("button")
        }
        
        if(!kMedoidsButton.classList.contains("selected_button")) {
            kMedoidsButton.classList.remove("button")
            kMedoidsButton.classList.add("selected_button")
        }
    }

    invalidRemovalButton.addEventListener('click', onClickValidationButton);
    invalidRemovalButton.classList.remove('disabled_button');
    invalidRemovalButton.classList.add('button');
    msAlgButton.addEventListener('click', onClickValidationButton);
    msAlgButton.classList.remove('disabled_button');
    msAlgButton.classList.add('button');

    document.getElementById("selected-clust").value = this.id;
    
}

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


