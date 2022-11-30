const email = localStorage.getItem("email");
const pwd = localStorage.getItem("pwd");
const selectedCampaign = localStorage.getItem("selectedCampaign");

console.log("Email: " + email)
console.log("Pwd: " + pwd)
console.log("Campagna: " + selectedCampaign);




const inputs = document.getElementsByClassName('campaign_input');

const proceedButton = document.getElementById('proceed-button');

proceedButton.addEventListener('click', onClickProceed);

function checkFilledInput() {
    for(var i = 0 ; i < inputs.length ; i++)
        if(inputs[i].value.length === 0)
            return false;   
    return true;
}

function onClickProceed() {
    if(checkFilledInput()) {
        var valInserted = []

        for(var i = 0 ; i < inputs.length ; i++)
            valInserted[i] = inputs[i].value

        localStorage.setItem("attrData", JSON.stringify(valInserted))

        location.href = "seclev";
    } else {
        alert("Fill every field before proceeding!");
    }    
}