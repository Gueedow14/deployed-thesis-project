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

    document.getElementById("loader-div").style.display = "flex"
    
    for(var i = 0 ; i<num_data ; i++) {
        var input = document.getElementById("data-" + (i+1))
        input.disabled = false;
    }
    
}


var attrDivs = document.getElementsByClassName("change_icon_div_attr");

for(var i = 0 ; i < attrDivs.length ; i++) {
    attrDivs[i].addEventListener('click', modifyAttrs);
}


function modifyAttrs() {
    var idLen = this.id.length;
    var inputId = "input-" + this.id.slice(7,idLen);
    var selectedInput = document.getElementById(inputId);
    selectedInput.disabled = false;
    selectedInput.setSelectionRange(selectedInput.value.length, selectedInput.value.length);
    selectedInput.focus()
    var attributeId = "attr-" + this.id.slice(7,idLen);
    var selectedAttribute = document.getElementById(attributeId);
    selectedAttribute.disabled = false;
}




