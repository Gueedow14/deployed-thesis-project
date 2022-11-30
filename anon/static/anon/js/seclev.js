const email = localStorage.getItem("email");
const pwd = localStorage.getItem("pwd");
const selectedCampaign = localStorage.getItem("selectedCampaign");
const attrData = JSON.parse(localStorage.getItem("attrData"));

console.log("Email: " + email)
console.log("Pwd: " + pwd)
console.log("Campagna: " + selectedCampaign);
console.log("Attr Data:\n")
for(var i = 0 ; i<attrData.length ; i++)
  console.log("   - " + attrData[i])




var slider = document.getElementById("myRange");
var value_output = document.getElementById("value");
var level_output = document.getElementById("sec-level-p");
var button = document.getElementById("confirm-button");
var confirmWindow = document.getElementById("window-confirm-security-value");
var iconForgot = document.getElementById('button-close-forgot');
var kValue = document.getElementById('k-value-confirm');

var value = 4;

value_output.innerHTML = value;


button.addEventListener('click', onClickButton);
iconForgot.addEventListener('click', onClickCloseIcon);



slider.oninput = function() {
  calcValue(this.value);
  value_output.innerHTML = value;
  setValueStyle();
}

function calcValue(n) {
	switch(true) {
  	case 0<n && n<=15: value = 1; break;
    case 15<n && n<=29: value = 2; break;
    case 29<n && n<=43: value = 3; break;
    case 43<n && n<=57: value = 4; break;
    case 57<n && n<=71: value = 5; break;
    case 71<n && n<=86: value = 6; break;
    case 86<n && n<=100: value = 7; break;
  }
}

function setValueStyle() {
  if(1<=value && value<=2) {
    level_output.innerHTML = "Low Security Level";
    level_output.style.color = "red";
  } else if(3<=value && value<=5) {
    level_output.innerHTML = "Mid Security Level";
    level_output.style.color = "#ffcc00";
  } else {
    level_output.innerHTML = "High Security Level";
    level_output.style.color = "green";
  }
}

function onClickButton() {
  confirmWindow.style.display = "block";
  kValue.innerHTML = value;

  if(1<=value && value<=2)
    kValue.style.color = "red";
  else if(3<=value && value<=5)
    kValue.style.color = "#ffcc00";
  else
    kValue.style.color = "green";
}

function onClickCloseIcon() {
  confirmWindow.style.display = 'none';
}

window.onclick = function(event) {
  if (event.target == confirmWindow) {
      confirmWindow.style.display = "none";
  }
} 


const windowConfirmButton = document.getElementById('window-confirm-button');

windowConfirmButton.addEventListener('click', confirmSecVal);

function confirmSecVal() {
  

  location.href = "homedataowner";
}