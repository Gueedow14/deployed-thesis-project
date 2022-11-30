var kgs = document.getElementById('kgs').children;
var kgsParent = document.getElementById('kgs');

var kgsIndexes = [];
 

$( document ).ready(function() {
    for(var i = 0 ; i < kgs.length ; i++) {
        kgs[i].id = "kg" + (i+1);
        kgsIndexes[i] = (i+1);
        kgs[i].addEventListener('click', onClickKG);
    }
});


function onClickKG() {
    if(!this.classList.contains("selected_kg")) {
        this.classList.add("selected_kg");
    } else {
        this.classList.remove("selected_kg");
    }
        
}




var sortButton = document.getElementById("sort-button");
var sortParams = document.getElementById("list-sort-params");
var chkOpenParams = false;
var selectedSortParam = document.getElementById("selected-sort-param");
var listSortParams = document.getElementsByClassName("sort_param");
var chkVisibleSelectedSortParam = false;
var filterButton = document.getElementById('filter-button');


filterButton.addEventListener('click', onClickFilter);
sortButton.addEventListener('click', onClickSort);
for(var i=0; i<listSortParams.length; i++)
    listSortParams[i].addEventListener('click', onClickParameter);



function onClickSort() {
    if(chkOpenParams) {
        sortParams.style.transform = "translateY(-400px)";
        chkOpenParams = false;
    } else {
        sortParams.style.transform = "translateY(0)";
        chkOpenParams = true;
    }
}

async function onClickParameter() {
    if(chkVisibleSelectedSortParam && this.innerHTML === "--Reset--") {
        selectedSortParam.style.opacity = "0";
        await new Promise(r => setTimeout(r, 200));
        selectedSortParam.innerHTML = this.innerHTML;
        chkVisibleSelectedSortParam = false;
        resetSort();
    } else if(!chkVisibleSelectedSortParam && this.innerHTML != "--Reset--") {
        selectedSortParam.style.opacity = "1";
        selectedSortParam.innerHTML = this.innerHTML;
        chkVisibleSelectedSortParam = true;
        callSortMethod(this.innerHTML);
    } else if (chkVisibleSelectedSortParam && this.innerHTML != "--Reset--") {
        selectedSortParam.innerHTML = this.innerHTML;
        callSortMethod(this.innerHTML);
    }
}

function callSortMethod(str) {
    switch(str) {
        case "Highest RRU": highestRRU(); break;
        case "Lowest RRU": lowestRRU(); break;
        case "Highest AIL": highestAIL(); break;
        case "Lowest AIL": lowestAIL(); break;
        case "Alphabetical": alphabetical(); break;
        case "Clustering Algorithm": clusteringAlg(); break;
        case "Validation Algorithm": validationAlg(); break;
        default: console.log("ERROR");
    }
}

function resetSort() {

    for(var i = 0 ; i < kgsIndexes.length ; i++) {
        for(var j = i ; j < kgsIndexes.length ; j++) {
            if(kgsIndexes[j] < kgsIndexes[i]) {
                kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));
                
                var tmp1 = kgsIndexes[i];
                kgsIndexes[i] = kgsIndexes[j];
                for(var count = i+1 ; count < j+1 ; count++) {
                    var tmp2 = kgsIndexes[count];
                    kgsIndexes[count] = tmp1;
                    tmp1 = tmp2;
                }

            }
        }
    }

}

function getRRUs() {
    var RRUs = [];

    for(var i = 0 ; i < kgs.length ; i++)
        RRUs[i] = kgs[i].children[1].children[0].children[1].lastChild.innerHTML;

    return RRUs;
}

function getAILs() {
    var AILs = [];

    for(var i = 0 ; i < kgs.length ; i++)
        AILs[i] = kgs[i].children[1].children[0].children[2].lastChild.innerHTML;

    return AILs;
}

function getNames() {
    var names = [];

    for(var i = 0 ; i < kgs.length ; i++)
        names[i] = kgs[i].children[1].children[0].children[0].innerHTML;

    return names;
}

function getClusteringAlgs() {
    var clustAlgs = [];

    for(var i = 0 ; i < kgs.length ; i++)
        clustAlgs[i] = kgs[i].children[1].children[0].children[3].lastChild.innerHTML;

    return clustAlgs;
}

function getValidationAlgs() {
    var valAlgs = [];

    for(var i = 0 ; i < kgs.length ; i++)
        valAlgs[i] = kgs[i].children[1].children[0].children[4].lastChild.innerHTML;

    return valAlgs;
}

function highestRRU() {
    var valuesRRU = getRRUs();
    
    for(var i = 0 ; i < valuesRRU.length ; i++) {
        for(var j = i ; j < valuesRRU.length ; j++) {
            if(parseFloat(valuesRRU[i]) < parseFloat(valuesRRU[j])) {
                kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));

                var tmp1 = valuesRRU[i];
                var tmp2;
                valuesRRU[i] = valuesRRU[j];
                for(var count = i+1 ; count < j+1 ; count++) {
                    tmp2 = valuesRRU[count];
                    valuesRRU[count] = tmp1;
                    tmp1 = tmp2;
                }

                
                
                tmp1 = kgsIndexes[i];
                kgsIndexes[i] = kgsIndexes[j];
                for(var count = i+1 ; count < j+1 ; count++) {
                    tmp2 = kgsIndexes[count];
                    kgsIndexes[count] = tmp1;
                    tmp1 = tmp2;
                }

            }
        }
    }
}

function lowestRRU() {
    var valuesRRU = getRRUs();

    for(var i = 0 ; i < valuesRRU.length ; i++) {
        for(var j = i ; j < valuesRRU.length ; j++) {
            if(parseFloat(valuesRRU[i]) > parseFloat(valuesRRU[j])) {
                kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));

                var tmp1 = valuesRRU[i];
                var tmp2;
                valuesRRU[i] = valuesRRU[j];
                for(var count = i+1 ; count < j+1 ; count++) {
                    tmp2 = valuesRRU[count];
                    valuesRRU[count] = tmp1;
                    tmp1 = tmp2;
                }

                
                
                tmp1 = kgsIndexes[i];
                kgsIndexes[i] = kgsIndexes[j];
                for(var count = i+1 ; count < j+1 ; count++) {
                    tmp2 = kgsIndexes[count];
                    kgsIndexes[count] = tmp1;
                    tmp1 = tmp2;
                }

            }
        }
    }
}



function highestAIL() {
    var valuesAIL = getAILs();

    for(var i = 0 ; i < valuesAIL.length ; i++) {
        for(var j = i ; j < valuesAIL.length ; j++) {
            if(parseFloat(valuesAIL[i]) < parseFloat(valuesAIL[j])) {
                kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));

                var tmp1 = valuesAIL[i];
                var tmp2;
                valuesAIL[i] = valuesAIL[j];
                for(var count = i+1 ; count < j+1 ; count++) {
                    tmp2 = valuesAIL[count];
                    valuesAIL[count] = tmp1;
                    tmp1 = tmp2;
                }

                
                
                tmp1 = kgsIndexes[i];
                kgsIndexes[i] = kgsIndexes[j];
                for(var count = i+1 ; count < j+1 ; count++) {
                    tmp2 = kgsIndexes[count];
                    kgsIndexes[count] = tmp1;
                    tmp1 = tmp2;
                }

            }
        }
    }
}  

function lowestAIL() {
    var valuesAIL = getAILs();

    for(var i = 0 ; i < valuesAIL.length ; i++) {
        for(var j = i ; j < valuesAIL.length ; j++) {
            if(parseFloat(valuesAIL[i]) > parseFloat(valuesAIL[j])) {
                kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));

                var tmp1 = valuesAIL[i];
                var tmp2;
                valuesAIL[i] = valuesAIL[j];
                for(var count = i+1 ; count < j+1 ; count++) {
                    tmp2 = valuesAIL[count];
                    valuesAIL[count] = tmp1;
                    tmp1 = tmp2;
                }

                
                
                tmp1 = kgsIndexes[i];
                kgsIndexes[i] = kgsIndexes[j];
                for(var count = i+1 ; count < j+1 ; count++) {
                    tmp2 = kgsIndexes[count];
                    kgsIndexes[count] = tmp1;
                    tmp1 = tmp2;
                }

            }
        }
    }
}









var ascOrDesc = true;
var ascOrDescClust = true;
var ascOrDescVal = true;


function alphabetical() {

    var names = getNames();

    if(ascOrDesc) {

        for(var i = 0 ; i < names.length ; i++) {
            for(var j = i ; j < names.length ; j++) {
                if(names[i] > names[j]) {

                    kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));
    
                    var tmp1 = names[i];
                    var tmp2;
                    names[i] = names[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = names[count];
                        names[count] = tmp1;
                        tmp1 = tmp2;
                    }

                    
                    
                    tmp1 = kgsIndexes[i];
                    kgsIndexes[i] = kgsIndexes[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = kgsIndexes[count];
                        kgsIndexes[count] = tmp1;
                        tmp1 = tmp2;
                    }
                }
            }
        }

        ascOrDesc = false;
        ascOrDescClust = true;
        ascOrDescVal = true;

    } else {

        for(var i = 0 ; i < names.length ; i++) {
            for(var j = i ; j < names.length ; j++) {
                if(names[i] < names[j]) {
                    kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));
    
                    var tmp1 = names[i];
                    var tmp2;
                    names[i] = names[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = names[count];
                        names[count] = tmp1;
                        tmp1 = tmp2;
                    }

                    
                    
                    tmp1 = kgsIndexes[i];
                    kgsIndexes[i] = kgsIndexes[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = kgsIndexes[count];
                        kgsIndexes[count] = tmp1;
                        tmp1 = tmp2;
                    }
                }
            }
        }

        ascOrDesc = true;
        ascOrDescClust = true;
        ascOrDescVal = true;

    }

}

function clusteringAlg() {

    var clusteringAlgs = getClusteringAlgs();

    if(ascOrDescClust) {

        for(var i = 0 ; i < clusteringAlgs.length ; i++) {
            for(var j = i ; j < clusteringAlgs.length ; j++) {
                if(clusteringAlgs[i] > clusteringAlgs[j]) {

                    kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));
    
                    var tmp1 = clusteringAlgs[i];
                    var tmp2;
                    clusteringAlgs[i] = clusteringAlgs[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = clusteringAlgs[count];
                        clusteringAlgs[count] = tmp1;
                        tmp1 = tmp2;
                    }

                    
                    
                    tmp1 = kgsIndexes[i];
                    kgsIndexes[i] = kgsIndexes[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = kgsIndexes[count];
                        kgsIndexes[count] = tmp1;
                        tmp1 = tmp2;
                    }
                }
            }
        }

        ascOrDesc = true;
        ascOrDescClust = false;
        ascOrDescVal = true;

    } else {

        for(var i = 0 ; i < clusteringAlgs.length ; i++) {
            for(var j = i ; j < clusteringAlgs.length ; j++) {
                if(clusteringAlgs[i] < clusteringAlgs[j]) {
                    kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));
    
                    var tmp1 = clusteringAlgs[i];
                    var tmp2;
                    clusteringAlgs[i] = clusteringAlgs[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = clusteringAlgs[count];
                        clusteringAlgs[count] = tmp1;
                        tmp1 = tmp2;
                    }

                    
                    
                    tmp1 = kgsIndexes[i];
                    kgsIndexes[i] = kgsIndexes[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = kgsIndexes[count];
                        kgsIndexes[count] = tmp1;
                        tmp1 = tmp2;
                    }
                }
            }
        }

        ascOrDesc = true;
        ascOrDescClust = true;
        ascOrDescVal = true;

    }

}

function validationAlg() {

    var validationAlgs = getValidationAlgs();

    if(ascOrDescVal) {

        for(var i = 0 ; i < validationAlgs.length ; i++) {
            for(var j = i ; j < validationAlgs.length ; j++) {
                if(validationAlgs[i] > validationAlgs[j]) {

                    kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));
    
                    var tmp1 = validationAlgs[i];
                    var tmp2;
                    validationAlgs[i] = validationAlgs[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = validationAlgs[count];
                        validationAlgs[count] = tmp1;
                        tmp1 = tmp2;
                    }

                    
                    
                    tmp1 = kgsIndexes[i];
                    kgsIndexes[i] = kgsIndexes[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = kgsIndexes[count];
                        kgsIndexes[count] = tmp1;
                        tmp1 = tmp2;
                    }

                }
            }
        }

        ascOrDesc = true;
        ascOrDescClust = true;
        ascOrDescVal = false;

    } else {

        for(var i = 0 ; i < validationAlgs.length ; i++) {
            for(var j = i ; j < validationAlgs.length ; j++) {
                if(validationAlgs[i] < validationAlgs[j]) {

                    kgsParent.insertBefore(document.getElementById("kg" + kgsIndexes[j]), document.getElementById("kg" + kgsIndexes[i]));
                    
                    var tmp1 = validationAlgs[i];
                    var tmp2;
                    validationAlgs[i] = validationAlgs[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = validationAlgs[count];
                        validationAlgs[count] = tmp1;
                        tmp1 = tmp2;
                    }

                    
                    
                    tmp1 = kgsIndexes[i];
                    kgsIndexes[i] = kgsIndexes[j];
                    for(var count = i+1 ; count < j+1 ; count++) {
                        tmp2 = kgsIndexes[count];
                        kgsIndexes[count] = tmp1;
                        tmp1 = tmp2;
                    }

                }
            }
        }

        ascOrDesc = true;
        ascOrDescClust = true;
        ascOrDescVal = true;

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


function getMaxRRU() {
    var valuesRRU = getRRUs();
    var max = parseFloat(valuesRRU[0]);
    for(var i = 0 ; i < valuesRRU.length ; i++)
        if(parseFloat(valuesRRU[i]) > max) 
            max = parseFloat(valuesRRU[i]) 

    return max;
}

function getMinRRU() {
    var valuesRRU = getRRUs();
    var min = parseFloat(valuesRRU[0]);
    for(var i = 0 ; i < valuesRRU.length ; i++)
        if(parseFloat(valuesRRU[i]) < min) 
            min = parseFloat(valuesRRU[i]) 

    return min;
}

function getMaxAIL() {
    var valuesAIL = getAILs();
    var max = parseFloat(valuesAIL[0]);
    for(var i = 0 ; i < valuesAIL.length ; i++)
        if(parseFloat(valuesAIL[i]) > max) 
            max = parseFloat(valuesAIL[i]) 

    return max;
}

function getMinAIL() {
    var valuesAIL = getAILs();
    var min = parseFloat(valuesAIL[0]);
    for(var i = 0 ; i < valuesAIL.length ; i++)
        if(parseFloat(valuesAIL[i]) < min) 
            min = parseFloat(valuesAIL[i]) 

    return min;
}


function onClickFilter() {
    sortParams.style.transform = "translateY(-400px)";
    chkOpenParams = false;

    minRRU.innerHTML = getMinRRU();
    maxRRU.innerHTML = getMaxRRU();
    minAIL.innerHTML = getMinAIL();
    maxAIL.innerHTML = getMaxAIL();

    sliderRRU.min = getMinRRU();
    sliderRRU.max = getMaxRRU();
    sliderAIL.min = getMinAIL();
    sliderAIL.max = getMaxAIL();

    if(filtersApplied[0] === false)
        sliderRRU.value = sliderRRU/2;
    if(filtersApplied[1] === false)
        sliderAIL.value = sliderAIL/2;

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

    numFiltersApplied = 0;

    for(var i = 0 ; i < kgs.length ; i++)
        document.getElementById("kg" + kgsIndexes[i]).style.display = "block";



    if(filtersApplied[0] === true) {

        numFiltersApplied++;

        var valuesRRU = getRRUs();

        if(filterRRUValue)
            for(var i = 0 ; i < valuesRRU.length ; i++) {
                if(parseFloat(valuesRRU[i]) > currentRRUValue) {
                    document.getElementById("kg" + kgsIndexes[i]).style.display = "none";
                }
            }   
        else
            for(var i = 0 ; i < valuesRRU.length ; i++) {
                if(parseFloat(valuesRRU[i]) < currentRRUValue) {
                    document.getElementById("kg" + kgsIndexes[i]).style.display = "none";
                }
            }    
        
        
    }

    if(filtersApplied[1] === true) {

        numFiltersApplied++;


        var valuesAIL = getAILs();

        if(filterAILValue)
            for(var i = 0 ; i < valuesAIL.length ; i++) {
                if(parseFloat(valuesAIL[i]) > currentAILValue) {
                    document.getElementById("kg" + kgsIndexes[i]).style.display = "none";
                }
            }          
        else
            for(var i = 0 ; i < valuesAIL.length ; i++) {
                if(parseFloat(valuesAIL[i]) < currentAILValue) {
                    document.getElementById("kg" + kgsIndexes[i]).style.display = "none";
                }
            }    


    }

    if(filtersApplied[2] === true) {

        numFiltersApplied++;

        
        var clustAlgs = getClusteringAlgs();

        for(var i = 0 ; i < clustAlgs.length ; i++)
            if(clustAlgs[i] != currentFilterClust)
                document.getElementById("kg" + kgsIndexes[i]).style.display = "none";
    
    }

    if(filtersApplied[3] === true) {

        numFiltersApplied++;

        var valAlgs = getValidationAlgs();

        for(var i = 0 ; i < valAlgs.length ; i++)
            if(valAlgs[i] != currentFilterValid)
                document.getElementById("kg" + kgsIndexes[i]).style.display = "none";

    }

    numFilters.style.opacity = 1;
    numFilters.innerHTML = numFiltersApplied;
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

    numFilters.style.opacity = 0;

    filtersApplied = [false, false, false, false];

    for(var i = 0 ; i < kgs.length ; i++)
        document.getElementById("kg" + kgsIndexes[i]).style.display = "block";

}


var proceedButton = document.getElementById("proceed-button");


proceedButton.addEventListener('click', onClickProceed);

function onClickProceed() {
    var selectedKGs = document.getElementsByClassName("selected_kg");
    console.log(selectedKGs.length);
    if(selectedKGs.length === 0)
        alert("You need to select at least one KG in order to proceed!");
    else {
        //data to be passed

        location.href = "compareresults";
    }
}
