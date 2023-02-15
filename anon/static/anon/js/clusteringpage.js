var hdbscanButton = document.getElementById('hdbscan-button');
var kMedoidsButton = document.getElementById('km-button');
var vacButton = document.getElementById('vac-button');

hdbscanButton.addEventListener('click', onClickClusteringButton);
kMedoidsButton.addEventListener('click', onClickClusteringButton);
vacButton.addEventListener('click', onClickClusteringButton);

const radioButtons = document.getElementsByClassName("radio_alg");

for(var i = 0 ; i < radioButtons.length ; i++) {
    radioButtons[i].addEventListener('click', onClickRadio)
}

selectedRadio = null;

function onClickClusteringButton() {

    if((this.id == "vac-button")) {

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

        document.getElementById("selected-clust").value = this.id.split("-")[0];

        selectedRadio.checked = false;
        selectedRadio = null

    } else if((this.id == "hdbscan-button")) {

        if(vacButton.classList.contains("selected_button")) {
            vacButton.classList.remove("selected_button")
            vacButton.classList.add("button")
        }

        if(hdbscanButton.classList.contains("button")) {
            hdbscanButton.classList.remove("button")
            hdbscanButton.classList.add("selected_button")
        }

        if(kMedoidsButton.classList.contains("selected_button")) {
            kMedoidsButton.classList.remove("selected_button")
            kMedoidsButton.classList.add("button")
        }

        document.getElementById("selected-clust").value = "hdbscan-min";

        selectedRadio = document.getElementById("hdbscan-min")
        selectedRadio.checked = true;
    } else {

        if(vacButton.classList.contains("selected_button")) {
            vacButton.classList.remove("selected_button")
            vacButton.classList.add("button")
        }

        if(hdbscanButton.classList.contains("selected_button")) {
            hdbscanButton.classList.remove("selected_button")
            hdbscanButton.classList.add("button")
        }

        if(kMedoidsButton.classList.contains("button")) {
            kMedoidsButton.classList.remove("button")
            kMedoidsButton.classList.add("selected_button")
        }

        document.getElementById("selected-clust").value = "km-min";

        selectedRadio = document.getElementById("km-min")
        selectedRadio.checked = true;
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

    document.getElementById("selected-clust").value = this.id;
    
}

document.getElementById("anon-button").addEventListener('click', showLoader)

function showLoader() {
    document.getElementById("loader-div").style.display = "flex";
}