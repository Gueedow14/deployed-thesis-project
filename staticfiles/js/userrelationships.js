var relButtons = document.getElementsByClassName("icona");

for(var i = 0 ; i < relButtons.length ; i++) {
    relButtons[i].addEventListener('click', clickRelButton);
}

function clickRelButton() {
    var tmp = this.parentElement.parentElement.parentElement.children[0].children[0].getAttribute("name")

    if(tmp[0] == 's')
        rel = tmp.slice(9,tmp.length);
    else
        rel = tmp.slice(11,tmp.length);

    if(this.classList.contains("bi-check") && !this.parentElement.classList.contains("selected")) {
        this.parentElement.classList.add("selected");
        this.parentElement.parentElement.children[1].classList.remove("deselected");
        this.parentElement.parentElement.parentElement.children[0].children[0].setAttribute("name","selected-"+rel);
    } else if(this.classList.contains("bi-x") && !this.parentElement.classList.contains("deselected")) {
        this.parentElement.classList.add("deselected");
        this.parentElement.parentElement.children[0].classList.remove("selected");
        this.parentElement.parentElement.parentElement.children[0].children[0].setAttribute("name","deselected-"+rel);
    }
}

var submitRelButton = document.getElementsByName("submit-button")[0];

submitRelButton.addEventListener('click', clickSubmitRelButton);

function clickSubmitRelButton() {
    var rel = this.id.slice(7,this.id.length);
    console.log(rel)
    var usersSelectedElements = document.getElementsByName("selected-" + rel);
    var usersSelected = []
    for(var i = 0 ; i < usersSelectedElements.length ; i++)
        usersSelected[i] = usersSelectedElements[i].innerHTML.replace(/^\s+|\s+$/g, '');
    var selectedUsers = "";
    for(var i = 0 ; i < usersSelected.length ; i++)
        selectedUsers += (usersSelected[i] + "|");
    console.log(selectedUsers)
    document.getElementById("selected-users").setAttribute("value", selectedUsers)
}



