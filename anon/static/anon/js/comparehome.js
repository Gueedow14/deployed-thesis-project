var table = document.getElementById("graph-table");
var rows = table.getElementsByTagName("tr");

for (i = 1; i < rows.length; i++) {
	rows[i].addEventListener('click', onClickRow)
}

selectedRows = []

function onClickRow() {
	
    if(selectedRows.includes(this.id)) {
        selectedRows = selectedRows.filter(selectedRows => selectedRows != this.id)
        this.style.color = "black"
        this.style.fontWeight = "100"
    } else {
        selectedRows.push(this.id)
        this.style.color = "red"
        this.style.fontWeight = "bold"
    }

}




var filterButton = document.getElementById('filter-button');
filterButton.addEventListener('click', onClickFilter);



var calgoColumn = document.getElementById('column-calgo');
var enforcerColumn = document.getElementById('column-enforcer');

calgoColumn.addEventListener('click', onClickTextColumn);
enforcerColumn.addEventListener('click', onClickTextColumn);

chkCalgoCol = false;
chkEnforcerCol = false;

var RRUColumn = document.getElementById('column-rru');
var AILColumn = document.getElementById('column-ail');

RRUColumn.addEventListener('click', onClickNumColumn);
AILColumn.addEventListener('click', onClickNumColumn);

chkRRUCol = false;
chkAILCol = false;

function onClickTextColumn() {

    if(this.id == 'column-calgo') {
        if(chkCalgoCol) {
            sortTableDesc(0);
            chkCalgoCol = false;
            calgoColumn.innerHTML = "Clustering Algorithm ▼"
        } else {
            sortTableAsc(0);
            chkCalgoCol = true;
            calgoColumn.innerHTML = "Clustering Algorithm ▲"
        }
        chkEnforcerCol = false;
        chkAILCol = false;
        chkRRUCol = false;
        enforcerColumn.innerHTML = "Validation Algorithm"
        RRUColumn.innerHTML = "RRU"
        AILColumn.innerHTML = "AIL"
    } else if(this.id == 'column-enforcer') {
        if(chkEnforcerCol) {
            sortTableDesc(1);
            chkEnforcerCol = false;
            enforcerColumn.innerHTML = "Validation Algorithm ▼"
        } else {
            sortTableAsc(1);
            chkEnforcerCol = true;
            enforcerColumn.innerHTML = "Validation Algorithm ▲"
        }
        chkCalgoCol = false;
        chkAILCol = false;
        chkRRUCol = false;
        calgoColumn.innerHTML = "Clustering Algorithm"
        RRUColumn.innerHTML = "RRU"
        AILColumn.innerHTML = "AIL"
    }


}


function sortTableAsc(column) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("graph-table");
    switching = true;
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
      //start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /*Loop through all table rows (except the
      first, which contains table headers):*/
      for (i = 1; i < (rows.length - 1); i++) {
        //start by saying there should be no switching:
        shouldSwitch = false;
        /*Get the two elements you want to compare,
        one from current row and one from the next:*/
        x = rows[i].getElementsByTagName("TD")[column];
        y = rows[i + 1].getElementsByTagName("TD")[column];
        //check if the two rows should switch place:
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            //if so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
}

function sortTableDesc(column) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("graph-table");
    switching = true;
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
      //start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /*Loop through all table rows (except the
      first, which contains table headers):*/
      for (i = 1; i < (rows.length - 1); i++) {
        //start by saying there should be no switching:
        shouldSwitch = false;
        /*Get the two elements you want to compare,
        one from current row and one from the next:*/
        x = rows[i].getElementsByTagName("TD")[column];
        y = rows[i + 1].getElementsByTagName("TD")[column];
        //check if the two rows should switch place:
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
}

function onClickNumColumn() {

    if(this.id == 'column-rru') {
        if(chkRRUCol) {
            sortTableNumDesc(2);
            chkRRUCol = false;
            RRUColumn.innerHTML = "RRU ▼"
        } else {
            sortTableNumAsc(2);
            chkRRUCol = true;
            RRUColumn.innerHTML = "RRU ▲"
        }
        chkAILCol = false;
        chkCalgoCol = false;
        chkEnforcerCol = false;
        AILColumn.innerHTML = "AIL"
        calgoColumn.innerHTML = "Clustering Algorithm"
        enforcerColumn.innerHTML = "Validation Algorithm"
    } else if(this.id == 'column-ail') {
        if(chkAILCol) {
            sortTableNumDesc(3);
            chkAILCol = false;
            AILColumn.innerHTML = "AIL ▼"
        } else {
            sortTableNumAsc(3);
            chkAILCol = true;
            AILColumn.innerHTML = "AIL ▲"
        }
        chkRRUCol = false;
        chkCalgoCol = false;
        chkEnforcerCol = false;
        RRUColumn.innerHTML = "RRU"
        calgoColumn.innerHTML = "Clustering Algorithm"
        enforcerColumn.innerHTML = "Validation Algorithm"
    }


}


function sortTableNumAsc(column) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("graph-table");
    switching = true;
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
      //start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /*Loop through all table rows (except the
      first, which contains table headers):*/
      for (i = 1; i < (rows.length - 1); i++) {
        //start by saying there should be no switching:
        shouldSwitch = false;
        /*Get the two elements you want to compare,
        one from current row and one from the next:*/
        x = rows[i].getElementsByTagName("TD")[column];
        y = rows[i + 1].getElementsByTagName("TD")[column];
        //check if the two rows should switch place:
        if (parseFloat(x.innerHTML.toLowerCase()) > parseFloat(y.innerHTML.toLowerCase())) {
            //if so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
}

function sortTableNumDesc(column) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("graph-table");
    switching = true;
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
      //start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /*Loop through all table rows (except the
      first, which contains table headers):*/
      for (i = 1; i < (rows.length - 1); i++) {
        //start by saying there should be no switching:
        shouldSwitch = false;
        /*Get the two elements you want to compare,
        one from current row and one from the next:*/
        x = rows[i].getElementsByTagName("TD")[column];
        y = rows[i + 1].getElementsByTagName("TD")[column];
        //check if the two rows should switch place:
        if (parseFloat(x.innerHTML.toLowerCase()) < parseFloat(y.innerHTML.toLowerCase())) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
}















var windowFilters = document.getElementById('window-filters');

var sliderRRU = document.getElementById('RRU-filter');
var sliderAIL = document.getElementById('AIL-filter');
var valueRRU = document.getElementById('RRU-current-value');
var valueAIL = document.getElementById('AIL-current-value');

var minRRU = document.getElementById('RRU-min');
var maxRRU = document.getElementById('RRU-max');
var minAIL = document.getElementById('AIL-min');
var maxAIL = document.getElementById('AIL-max');

var buttonVAC = document.getElementById('filter-vac');
var buttonKMedoids = document.getElementById('filter-k-medoids');
var buttonHDBSCAN = document.getElementById('filter-hdbscan');

var buttonInvalidRemoval = document.getElementById('filter-invalid-removal');
var buttonMSAlgorithm = document.getElementById('filter-ms-alg');

var numFilters = document.getElementById("num-filters");

var numFiltersApplied = 0;
var filtersApplied = [false, false, false, false];




function onClickFilter() {

    minRRU.innerHTML = getMinRRU();
    maxRRU.innerHTML = getMaxRRU();
    minAIL.innerHTML = getMinAIL();
    maxAIL.innerHTML = getMaxAIL();

    sliderRRU.min = getMinRRU();
    sliderRRU.max = getMaxRRU();
    sliderAIL.min = getMinAIL();
    sliderAIL.max = getMaxAIL();

    if(filtersApplied[0] === false)
        sliderRRU.value = (sliderRRU.max + sliderRRU.min)/2;
    if(filtersApplied[1] === false)
        sliderAIL.value = (sliderAIL.max + sliderAIL.min)/2;

    windowFilters.style.display = "block";
}

window.onclick = function(event) {
    if (event.target == document.getElementById('window-filters')) {
        windowFilters.style.display = "none";
    }
}

var currentRRUValue, currentAILValue;

sliderRRU.oninput = function() {
    valueRRU.style.display = "block";
    currentRRUValue = parseFloat(this.value);
    valueRRU.innerHTML = this.value + " or less";
    filtersApplied[0] = true;
}

sliderAIL.oninput = function() {
    valueAIL.style.display = "block";
    currentAILValue = parseFloat(this.value);
    valueAIL.innerHTML = this.value + " or less";
    filtersApplied[1] = true;
}


valueRRU.addEventListener('click', changeRRUFilter);
valueAIL.addEventListener('click', changeAILFilter);




var filterRRUValue = true; //true=less
var filterAILValue = true; //true=less


function changeRRUFilter() {
    if(filterRRUValue) {
        valueRRU.innerHTML = currentRRUValue + " or more";
        filterRRUValue = false;
    } else {
        valueRRU.innerHTML = currentRRUValue + " or less";
        filterRRUValue = true;
    }
}

function changeAILFilter() {
    if(filterAILValue) {
        valueAIL.innerHTML = currentAILValue + " or more";
        filterAILValue = false;
    } else {
        valueAIL.innerHTML = currentAILValue + " or less";
        filterAILValue = true;
    }
}







buttonVAC.addEventListener('click', setFilterClust);
buttonKMedoids.addEventListener('click', setFilterClust);
buttonHDBSCAN.addEventListener('click', setFilterClust);

buttonInvalidRemoval.addEventListener('click', setFilterValid);
buttonMSAlgorithm.addEventListener('click', setFilterValid);

var currentFilterClust;

function setFilterClust() {
    filtersApplied[2] = true;
    currentFilterClust = this.parentElement.children[0].innerHTML;
}

var currentFilterValid;

function setFilterValid() {
    filtersApplied[3] = true;
    currentFilterValid = this.parentElement.children[0].innerHTML;
}






var setFiltersButton = document.getElementById('filters-button');

setFiltersButton.addEventListener('click', setFilters);


function setFilters() {

    for(var i = 1 ; i < rows.length ; i++)
        document.getElementById("row-" + i).style.display = "table-row";


    if(filtersApplied[0] === true) {

        for (i = 1; i < rows.length; i++) {
            td = rows[i].getElementsByTagName("td")[2];
            if(td) {
                txtValue = parseFloat(td.textContent || td.innerText);
                console.log(txtValue)

                if(filterRRUValue) {    //equal or less

                    if(txtValue <= currentRRUValue && rows[i].style.display != "none") {
                        rows[i].style.display = "";
                    } else {
                        rows[i].style.display = "none";
                    }

                } else {                //equal or more

                    if(txtValue >= currentRRUValue && rows[i].style.display != "none") {
                        rows[i].style.display = "";
                    } else {
                        rows[i].style.display = "none";
                    }

                }

            }
        }

    }

    if(filtersApplied[1] === true) {

        for (i = 1; i < rows.length; i++) {
            td = rows[i].getElementsByTagName("td")[3];
            if(td) {
                txtValue = parseFloat(td.textContent || td.innerText);
                console.log(txtValue)

                if(filterRRUValue) {    //equal or less

                    if(txtValue <= currentAILValue && rows[i].style.display != "none") {
                        rows[i].style.display = "";
                    } else {
                        rows[i].style.display = "none";
                    }

                } else {                //equal or more

                    if(txtValue >= currentAILValue && rows[i].style.display != "none") {
                        rows[i].style.display = "";
                    } else {
                        rows[i].style.display = "none";
                    }

                }

            }
        }

    }

    if(filtersApplied[2] === true) {

        for (i = 1; i < rows.length; i++) {
            td = rows[i].getElementsByTagName("td")[0];
            if(td) {
                txtValue = (td.textContent || td.innerText).split("#")[0];
                console.log(txtValue)

                if(txtValue === currentFilterClust && rows[i].style.display != "none") {
                    rows[i].style.display = "";
                } else {
                    rows[i].style.display = "none";
                }

            }
        }
    }

    if(filtersApplied[3] === true) {

        for (i = 1; i < rows.length; i++) {
            td = rows[i].getElementsByTagName("td")[1];
            if(td) {
                txtValue = (td.textContent || td.innerText).split("#")[0];
                console.log(txtValue)

                if(txtValue === currentFilterValid && rows[i].style.display != "none") {
                    rows[i].style.display = "";
                } else {
                    rows[i].style.display = "none";
                }

            }
        }
        
    }


    windowFilters.style.display = "none";

}




var resetFiltersButton = document.getElementById('reset-button');
resetFiltersButton.addEventListener('click', resetFilters);

function resetFilters() {
    sliderRRU.value = sliderRRU/2;
    valueRRU.innerHTML = sliderRRU/2;
    valueRRU.style.display = "none";

    sliderAIL.value = sliderAIL/2;
    valueAIL.innerHTML = sliderAIL/2;
    valueAIL.style.display = "none";

    var radios = document.getElementsByClassName('radio_alg');

    for(var i = 0; i<radios.length; i++)
        if(radios[i].checked === true)
            radios[i].checked = false;    

    filtersApplied = [false, false, false, false];

    for(var i = 1 ; i < rows.length ; i++)
        document.getElementById("row-" + i).style.display = "table-row";

}


const inputProceed = document.getElementById("selected-graphs-input");

const proceedButton = document.getElementById("proceed-button");
proceedButton.addEventListener('click', onClickProceed);

function onClickProceed() {
    tmp = ""

    if(selectedRows.length === 0)
        alert("You need to select at least one Row in order to proceed!");
    else
        for(var i = 0 ; i<selectedRows.length ; i++) {
            thisRow = document.getElementById(selectedRows[i]);
            values = thisRow.getElementsByTagName("TD");
            for(var j = 0 ; j<values.length ; j++)
                tmp += (values[j].innerHTML + ";")
            tmp = tmp.slice(0,-1);
            tmp += "|"
        }
    tmp = tmp.slice(0,-1);
    inputProceed.value = tmp
}
