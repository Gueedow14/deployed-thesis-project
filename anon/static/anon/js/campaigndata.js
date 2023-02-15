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
    if(!checkFilledInput())
        alert("Fill every field before proceeding!");
}

proceedButton.addEventListener('click', onClickConfirm)

function onClickConfirm() {
  document.getElementById("loader-div").style.display = "flex"
}