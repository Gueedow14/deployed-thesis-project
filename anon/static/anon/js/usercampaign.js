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
