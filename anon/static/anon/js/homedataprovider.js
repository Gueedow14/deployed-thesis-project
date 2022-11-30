const exitButton = document.getElementById("exit-button");

exitButton.addEventListener('click', logout);

function logout() {
    //logout

    location.href = "logreg"
}



const createButton = document.getElementById('button-create');

createButton.addEventListener('click', createCampaign);

function createCampaign() {
    //data to be passed  -  idk if there'll be any

    location.href = "createcampaign";
}

var campaignList = document.getElementsByClassName('campaign');

for(var i = 0 ; i < campaignList.length ; i++) {
    campaignList[i].id = "campaign-" + (i+1);
    campaignList[i].addEventListener('click', selectCampaign);
}

function selectCampaign() {
    //data to be passed (campaign info)

    location.href = "campaignpage";
}