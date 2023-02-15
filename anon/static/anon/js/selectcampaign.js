var campaigns = document.getElementsByClassName("campaign"); 
var confirmButton = document.getElementById("button-confirm-choice");

var selectedCampaign = null;

for (var i = 0; i < campaigns.length; i++) {
    campaigns[i].addEventListener('click', onClickCampaign);
}

confirmButton.addEventListener('click', onClickConfirmButton);


function onClickCampaign() {
    if($('#' + this.id).hasClass("campaign") & selectedCampaign === null) {
        $('#' + this.id).removeClass("campaign");
        $('#' + this.id).addClass("selected_campaign");

        document.getElementById("input-campaign").value = this.children[0].textContent;

        selectedCampaign = this;

    } else if ($('#' + this.id).hasClass("selected_campaign")) {
        $('#' + this.id).removeClass("selected_campaign");
        $('#' + this.id).addClass("campaign");

        document.getElementById("input-campaign").value = "";

    } else if ($('#' + this.id).hasClass("campaign") & selectedCampaign != null) {
        $('#' + selectedCampaign.id).removeClass("selected_campaign");
        $('#' + selectedCampaign.id).addClass("campaign");
        $('#' + this.id).removeClass("campaign");
        $('#' + this.id).addClass("selected_campaign");

        document.getElementById("input-campaign").value = this.children[0].textContent;

        selectedCampaign = this;

    }
}

function onClickConfirmButton() {
    if(selectedCampaign == null || $('#' + selectedCampaign.id).hasClass("campaign")) {
        alert("No campaign selected");
        selectedCampaign = null;
    }
}

document.getElementById("button-confirm-choice").addEventListener('click', onClickConfirm)

function onClickConfirm() {
  document.getElementById("loader-div").style.display = "flex"
}