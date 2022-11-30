const email = localStorage.getItem("email");
const pwd = localStorage.getItem("pwd");

console.log("Email: " + email)
console.log("Pwd: " + pwd)



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
        selectedCampaign = this;
    } else if ($('#' + this.id).hasClass("selected_campaign")) {
        $('#' + this.id).removeClass("selected_campaign");
        $('#' + this.id).addClass("campaign");
    } else if ($('#' + this.id).hasClass("campaign") & selectedCampaign != null) {
        $('#' + selectedCampaign.id).removeClass("selected_campaign");
        $('#' + selectedCampaign.id).addClass("campaign");
        $('#' + this.id).removeClass("campaign");
        $('#' + this.id).addClass("selected_campaign");
        selectedCampaign = this;
    }
}

function onClickConfirmButton() {
    if(selectedCampaign != null & $('#' + selectedCampaign.id).hasClass("selected_campaign")) {
        localStorage.setItem("selectedCampaign", selectedCampaign.id);
        location.href = "campaigndata";
    } else {
        alert("No campaign selected");
        selectedCampaign = null;
    }
        
}
