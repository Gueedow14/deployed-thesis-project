const dataDiv = document.getElementById("data-div");
const num_data = 5;

for(var i = 0; i < num_data ; i++) {

    var container = document.createElement("div");
    container.classList.add("data_container");

    var divLabel = document.createElement("div");
    divLabel.classList.add("data_label");
    var label = document.createElement("label");
    var labelText = document.createTextNode("Data " + (i+1) +":")

    var divInput = document.createElement("div");
    var input = document.createElement("input");
    input.id = "data-" + (i+1);
    input.name = "data";
    input.disabled = true;
    input.classList.add("campaign_input");

    var divButton = document.createElement("div");
    divButton.classList.add("change_icon_div");
    var button = document.createElement("i");
    button.classList.add("change_icon");
    button.classList.add("bi");
    button.classList.add("bi-pencil");


    label.appendChild(labelText);

    divInput.appendChild(input);
    divLabel.appendChild(label);
    divButton.appendChild(button);

    container.appendChild(divLabel);
    container.appendChild(divInput);
    container.appendChild(divButton);

    dataDiv.append(container);

}





var chkPwd = false;     //false: pwd not visible

const pwd = document.getElementById("pwd");
const pwdIconDivSee = document.getElementById("pwd-icon-div-see");
const pwdIconSee = document.getElementById("pwd-icon-see");

pwdIconDivSee.addEventListener('click', changeVisibility);

function changeVisibility() {
    if(chkPwd) {
        pwdIconSee.classList.remove("bi-eye-slash-fill");
        pwdIconSee.classList.add("bi-eye-fill");
        pwd.setAttribute("type","password");
        chkPwd = false;
    } else {
        pwdIconSee.classList.remove("bi-eye-fill");
        pwdIconSee.classList.add("bi-eye-slash-fill");
        pwd.setAttribute("type","text");
        chkPwd = true;
    }
}

const windowChangePwd = document.getElementById("id-window-change");

const pwdIconDivChange = document.getElementById("pwd-icon-div-change");
const pwdIconChange = document.getElementById("pwd-icon-change");

const iconClose = document.getElementById("button-close");

pwdIconDivChange.addEventListener('click', openWindow);
iconClose.addEventListener('click', closeWindow);


function openWindow() {
    windowChangePwd.style.display = "flex";
}

function closeWindow() {
    windowChangePwd.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == windowChangePwd)
        closeWindow();
}

const doneButton = document.getElementById('button');

doneButton.addEventListener('click', applyChanges);

function applyChanges() {

    for(var i = 0 ; i<num_data ; i++) {
        var input = document.getElementById("data-" + (i+1))
        input.disabled = false;
    }
    
}


var dataDivs = document.getElementsByClassName("change_icon_div");
var dataInputs = document.getElementsByClassName("campaign_input");


for(var i = 0 ; i < dataDivs.length ; i++) {
    dataDivs[i].id = "data-" + (i+1) + "-icon-change";
    dataDivs[i].addEventListener('click', modifyData);
    dataInputs[i].id = "data-" + (i+1);
}


function modifyData() {
    var inputId = this.id.slice(0,6);
    var selectedInput = document.getElementById(inputId);
    selectedInput.disabled = false;
}


