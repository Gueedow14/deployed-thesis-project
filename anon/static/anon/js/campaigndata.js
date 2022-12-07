const dataDiv = document.getElementById("data-div");
const num_data = 3;

for(var i = 0; i < num_data ; i++) {

    var container = document.createElement("div");
    container.classList.add("data_container");

    var divLabel = document.createElement("div");
    divLabel.classList.add("data_label");
    var label = document.createElement("label");
    var labelText = document.createTextNode("Data " + (i+1) +":")

    var divInput = document.createElement("div");
    divInput.classList.add("data_input");
    var input = document.createElement("input");
    input.id = "data-" + (i+1);
    input.name = "data";
    input.autocomplete = "off";
    input.classList.add("campaign_input");


    label.appendChild(labelText);

    divInput.appendChild(input);
    divLabel.appendChild(label);

    container.appendChild(divLabel);
    container.appendChild(divInput);

    dataDiv.appendChild(container);

}




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