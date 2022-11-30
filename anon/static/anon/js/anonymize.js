document.getElementById("anonymize-button-container").style.display = "none";


var hdbscanButton = document.getElementById('hdbscan-button');
var kMedoidsButton = document.getElementById('k-medoids-button');
var vacButton = document.getElementById('vac-button');

hdbscanButton.addEventListener('click', onClickClusteringButton);
kMedoidsButton.addEventListener('click', onClickClusteringButton);
vacButton.addEventListener('click', onClickClusteringButton);

/*
hdbscanButton.addEventListener('click', onClickHDBSCAN);
kMedoidsButton.addEventListener('click', onClickKMedoids);
vacButton.addEventListener('click', onClickVAC);
*/


var invalidRemovalButton = document.getElementById('invalid-removal-button');
var msAlgButton = document.getElementById('ms-alg-button');


/*
invalidRemovalButton.addEventListener('click', onClickInvalidRemoval);
msAlgButton.addEventListener('click', onClickMSAlg);
*/



var clusteringOpen = false;

function onClickClusteringButton() {

    if(!clusteringOpen) {
        $("#clustering-kgs-container").slideDown("slow");
        clusteringOpen = true;
        invalidRemovalButton.addEventListener('click', onClickValidationButton);
        invalidRemovalButton.classList.remove('disabled_button');
        invalidRemovalButton.classList.add('button');
        msAlgButton.addEventListener('click', onClickValidationButton);
        msAlgButton.classList.remove('disabled_button');
        msAlgButton.classList.add('button');
    }

}

var validationOpen = false;

function onClickValidationButton() {

    if(!validationOpen) {
        $("#validation-kgs-container").slideDown("slow");
        validationOpen = true;
    }
    
}


var kgsClustContainer = document.getElementById("clustering-kgs");
var kgsValidContainer = document.getElementById("validation-kgs");

var listClustKG = kgsClustContainer.children;
var listValidKG = kgsValidContainer.children;


for(var i = 0 ; i<listClustKG.length ; i++) {
    listClustKG[i].addEventListener('click', onClickClustKG);
    listClustKG[i].id = "clustKG" + (i+1);
}
    

for(var i = 0 ; i<listValidKG.length ; i++) {
    listValidKG[i].addEventListener('click', onClickValidKG);
    listValidKG[i].id = "validKG" + (i+1);
}


var selectedClustKG = null;
var selectedValidKG = null;


function onClickClustKG() {

    if(selectedClustKG === null) {
        this.classList.remove("kg");
        this.classList.add("selected_kg");
        selectedClustKG = this;
    } else {
        selectedClustKG.classList.remove("selected_kg");
        selectedClustKG.classList.add("kg");
        this.classList.remove("kg");
        this.classList.add("selected_kg");
        selectedClustKG = this;
    }

    if(selectedValidKG != null & selectedClustKG != null) {
        $("#container").slideDown("slow");
        document.getElementById("anonymize-text-div").style.display = "block";
        $("#generalization-kgs-container").slideDown("slow");
        document.getElementById("anonymize-button-container").style.display = "block";
    }
}

function onClickValidKG() {

    if(selectedValidKG === null) {
        this.classList.remove("kg");
        this.classList.add("selected_kg");
        selectedValidKG = this;
    } else {
        selectedValidKG.classList.remove("selected_kg");
        selectedValidKG.classList.add("kg");
        this.classList.remove("kg");
        this.classList.add("selected_kg");
        selectedValidKG = this;
    }

    if(selectedValidKG != null & selectedClustKG != null) {
        $("#container").slideDown("slow");
        document.getElementById("anonymize-text-div").style.display = "block";
        $("#generalization-kgs-container").slideDown("slow");
        document.getElementById("anonymize-button-container").style.display = "block";
    }

}



var kgsGeneralizationContainer = document.getElementById("anonymization-kgs");

var listGenKG = kgsGeneralizationContainer.children;

for(var i = 0 ; i<listGenKG.length ; i++) {
    listGenKG[i].addEventListener('click', onClickGenKG);
    listGenKG[i].id = "genKG" + (i+1);
}

var selectedGenKG = null;

function onClickGenKG() {

    if(selectedGenKG === null) {
        this.classList.remove("kg");
        this.classList.add("selected_kg");
        document.getElementById("anon-button").classList.remove("disabled_button");
        document.getElementById("anon-button").classList.add("button");
        selectedGenKG = this;
    } else {
        selectedGenKG.classList.remove("selected_kg");
        selectedGenKG.classList.add("kg");
        this.classList.remove("kg");
        this.classList.add("selected_kg");
        selectedGenKG = this;
    }

}



const anonButton = document.getElementById('anon-button');

anonButton.addEventListener('click', anonymize);

function anonymize() {
    //code of anonymization

    location.href = "homedataprovider";
}


