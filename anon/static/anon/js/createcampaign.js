var dataList = document.getElementById("list");
var dataNum = dataList.getElementsByTagName("li").length;


$( document ).ready( 
    function() {
        if(dataNum == 0) {
            dataList.style.display = "none";
        }
    }
);


var attrButton = document.getElementById("attr-button");
var relButton = document.getElementById("rel-button");
var noDataDiv = document.getElementById("no-data-div");
var noData = document.getElementById("no-data-p");

var attrNameDiv = document.getElementById("attr-name-div");
var relNameDiv = document.getElementById("rel-name-div");
var attrName = document.getElementById("attr-name");
var relName = document.getElementById("rel-name");
var attrNameButton = document.getElementById("attr-name-button");
var relNameButton = document.getElementById("rel-name-button");


var listDataId = [];
var listDataNames = ["***ERROR***"];


attrButton.addEventListener('click', openAttrNameWindow);
relButton.addEventListener('click', openRelNameWindow);
attrNameButton.addEventListener('click', addAttribute);
relNameButton.addEventListener('click', addRelationship);



function openAttrNameWindow() {
    attrNameDiv.style.display = "block";
}

function openRelNameWindow() {
    relNameDiv.style.display = "block";
}

window.onclick = function(event) {
    if (event.target == attrNameDiv || event.target == relNameDiv || event.target == modAttrNameDiv || event.target == modRelNameDiv) {
        attrNameDiv.style.display = "none";
        attrName.value = "";
        relNameDiv.style.display = "none";
        relName.value = "";
        modAttrNameDiv.style.display = "none";
        modAttrName.value = "";
        modRelNameDiv.style.display = "none";
        modRelName.value = "";
    }
}

function addAttribute() {
    if(dataNum == 0) {
        noDataDiv.style.display = "none";
        dataList.style.display = "block";
    }
    const data = document.createElement("li");
    data.id = setId("Attribute");
    dataList.appendChild(data);

    const name = document.createElement("span");
    name.innerText = setName(attrName.value);
    if(name.innerHTML == "***ERROR***") {
        if(dataNum == 0) {
            noDataDiv.style.display = "block";
            dataList.style.display = "none";
        }
        dataList.removeChild(data);
        return;
    }
    name.classList.add("data_name");
    name.style.color = "blue";
    data.appendChild(name);

    const modify = document.createElement("span");
    modify.id = setId("pencil-emoji");
    modify.classList.add("data_modify");
    data.appendChild(modify);
    modify.addEventListener('click', modifyAttr);

    const emojiPencil = document.createElement("i");
    emojiPencil.classList.add("bi");
    emojiPencil.classList.add("bi-pencil");
    modify.appendChild(emojiPencil);

    const del = document.createElement("span");
    del.id = setId("bin-emoji");
    del.classList.add("data_delete");
    data.appendChild(del);
    del.addEventListener('click', removeAttr);

    const emojiBin = document.createElement("i");
    emojiBin.classList.add("bi");
    emojiBin.classList.add("bi-trash3");
    del.appendChild(emojiBin);



    dataNum++;
    attrNameDiv.style.display = "none";
    attrName.value = "";
}







function addRelationship() {
    if(dataNum == 0) {
        noDataDiv.style.display = "none";
        dataList.style.display = "block";
    }
    const data = document.createElement("li");
    data.id = setId("Relationship");
    dataList.appendChild(data);

    const name = document.createElement("span");
    name.innerText = setName(relName.value);
    if(name.innerHTML == "***ERROR***") {
        if(dataNum == 0) {
            noDataDiv.style.display = "block";
            dataList.style.display = "none";
        }
        dataList.removeChild(data);
        return;
    }
    name.classList.add("data_name");
    name.style.color = "red";
    data.appendChild(name);

    const modify = document.createElement("span");
    modify.id = setId("pencil-emoji");
    modify.classList.add("data_modify");
    data.appendChild(modify);
    modify.addEventListener('click', modifyRel);

    const emojiPencil = document.createElement("i");
    emojiPencil.classList.add("bi");
    emojiPencil.classList.add("bi-pencil");
    modify.appendChild(emojiPencil);

    const del = document.createElement("span");
    del.id = setId("bin-emoji");
    del.classList.add("data_delete");
    data.appendChild(del);
    del.addEventListener('click',removeRel);

    const emojiBin = document.createElement("i");
    emojiBin.classList.add("bi");
    emojiBin.classList.add("bi-trash3");
    del.appendChild(emojiBin);



    dataNum++;
    relNameDiv.style.display = "none";
    relName.value = "";
}

function setId(str) {
    var i = 1;

    if(listDataId.includes(str)) {
        do {
            if(i == 1)
                str = str + "" + i;
            else {
                var tmp = str.split('');
                tmp.splice(str.length - 1 , 1);
                str = tmp.join('');
                str = str + "" + i;
            }
            i++;
        } while(listDataId.includes(str));
    }

    listDataId.push(str);

    return str;
}

function setName(str) {
    if(!listDataNames.includes(str) && isValidName(str)) {
        listDataNames.push(str);
        return str;
    }

    alert("This name is not valid, write something else.");

    attrName.value = "";
    relName.value = "";

    return "***ERROR***";
}



function removeAttr() {
    var li = document.getElementById(this.parentElement.id);

    var count = 0;
    while(listDataNames[count] != li.firstChild.innerHTML)
        count++;
    listDataNames.splice(count, 1);

    while (li.firstChild) {
        li.removeChild(li.lastChild);
    }
    li.remove();
    
    if(--dataNum == 0) {
        noDataDiv.style.display = "block";
        dataList.style.display = "none";
    }
}


function removeRel() {
    var li = document.getElementById(this.parentElement.id);

    var count = 0;
    while(listDataNames[count] != li.firstChild.innerHTML)
        count++;
    listDataNames.splice(count, 1);

    while (li.firstChild) {
        li.removeChild(li.lastChild);
    }
    li.remove();
    
    if(--dataNum == 0) {
        noDataDiv.style.display = "block";
        dataList.style.display = "none";
    }
}


var modAttrNameDiv = document.getElementById("mod-attr-name-div");
var modRelNameDiv = document.getElementById("mod-rel-name-div");
var modAttrName = document.getElementById("mod-attr-name");
var modRelName = document.getElementById("mod-rel-name");
var modAttrNameButton = document.getElementById("mod-attr-name-button");
var modRelNameButton = document.getElementById("mod-rel-name-button");

var selectedLi = null;


modAttrNameButton.addEventListener('click', applyModAttr);
modRelNameButton.addEventListener('click', applyModRel);


function modifyAttr() {
    modAttrNameDiv.style.display = "block";
    selectedLi = this.parentElement;
}

function modifyRel() {
    modRelNameDiv.style.display = "block";
    selectedLi = this.parentElement;
}

function applyModAttr() {
    var currentName = selectedLi.firstChild.innerHTML;

    var count = 0;
    while(listDataNames[count] != selectedLi.firstChild.innerHTML)
        count++;
    listDataNames.splice(count, 1);

    selectedLi.firstChild.innerHTML = setName(modAttrName.value);
    if(selectedLi.firstChild.innerHTML == "***ERROR***") {
        selectedLi.firstChild.innerHTML = currentName;
        listDataNames.push(currentName);
        modAttrName.value = "";
        return;
    }

    modAttrName.value = "";

    modAttrNameDiv.style.display = "none";
}

function applyModRel() {
    var currentName = selectedLi.firstChild.innerHTML;

    var count = 0;
    while(listDataNames[count] != selectedLi.firstChild.innerHTML)
        count++;
    listDataNames.splice(count, 1);

    selectedLi.firstChild.innerHTML = setName(modRelName.value);
    if(selectedLi.firstChild.innerHTML == "***ERROR***") {
        selectedLi.firstChild.innerHTML = currentName;
        listDataNames.push(currentName);
        modRelName.value = "";
        return;
    }

    modRelName.value = "";

    modRelNameDiv.style.display = "none";
}

var createButton = document.getElementById("create-campaign-button");

createButton.addEventListener('click', createCampaign);

function createCampaign() {
    if(dataNum == 0) {
        alert("A campaign requires data in order to be created!");
        return;
    } else {
        //create in db

        location.href = "homedataprovider";
    }
}

function isValidName(str) {
    //check if it's only spaces
    return str.trim().length != 0;
}