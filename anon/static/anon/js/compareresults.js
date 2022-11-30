var tableBox = document.getElementById("tableBox");
var table = document.getElementById("myTable");


var chartBox = document.getElementById("chartBox");
var chart = document.getElementById("myChart");


var names = ["KG1", "KG2", "KG3", "KG4"];
var RRUs = [1.7, 1.3, 3.1, 2.4];
var AILs = [3.7, 2.1, 2.9, 1.5];
var clustAlgs = ["VAC", "k-Medoids", "VAC", "HDBSCAN"];
var validAlgs = ["MS-Algorithm", "Invalid Removal", "Invalid Removal", "MS-Algorithm"];


for(var i = 0 ; i<names.length ; i++) {

    var row = document.createElement('tr');

    var n = document.createTextNode(names[i]);
    var RRU = document.createTextNode(RRUs[i]);
    var AIL = document.createTextNode(AILs[i]);
    var clustAlg = document.createTextNode(clustAlgs[i]);
    var validAlg = document.createTextNode(validAlgs[i]);

    for(var j = 0 ; j<5 ; j++) {

        var elem = document.createElement('td');

        switch(j) {
            case 0: elem.appendChild(n);
                    break;
            case 1: elem.appendChild(RRU);
                    break;
            case 2: elem.appendChild(AIL);
                    break;
            case 3: elem.appendChild(clustAlg);
                    break;
            case 4: elem.appendChild(validAlg);
                    break;
        }

        row.appendChild(elem);

    }
    
    table.children[0].appendChild(row);

}




const data = {
    labels: names,
    datasets: [{
        label: 'RRU',
        data: RRUs,
        backgroundColor: [
            'rgba(255, 0, 0, 0.2)',
            'rgba(255, 0, 0, 0.2)',
            'rgba(255, 0, 0, 0.2)',
            'rgba(255, 0, 0, 0.2)'
        ],
        borderColor: [
            'rgba(255, 0, 0, 1)',
            'rgba(255, 0, 0, 1)',
            'rgba(255, 0, 0, 1)',
            'rgba(255, 0, 0, 1)'
        ],
        borderWidth: 1.5
    } , 
    {
        label: 'AIL',
        data: AILs,
        backgroundColor: [
            'rgba(0, 0, 255, 0.2)',
            'rgba(0, 0, 255, 0.2)',
            'rgba(0, 0, 255, 0.2)',
            'rgba(0, 0, 255, 0.2)'
        ],
        borderColor: [
            'rgba(0, 0, 255, 1)',
            'rgba(0, 0, 255, 1)',
            'rgba(0, 0, 255, 1)',
            'rgba(0, 0, 255, 1)'
        ],
        borderWidth: 1.5
    }
]
};

// config 
const config = {
    type: 'bar',
    data,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
};

// render init block
const myChart = new Chart( document.getElementById('myChart') , config );










var toggleButton = document.getElementById('toggle-button');

toggleButton.addEventListener('click', onClickToggle);

async function onClickToggle() {

    if(this.checked) {

        chartBox.style.animation = "chartOutAnim .7s ease 1";
        chartBox.style.display = "none";
        tableBox.style.display = "flex";
        tableBox.style.animation = "tableInAnim .7s ease 1";

    } else {

        tableBox.style.animation = "tableOutAnim .7s ease 1";
        tableBox.style.display = "none";
        chartBox.style.display = "block";
        chartBox.style.animation = "chartInAnim .7s ease 1";

    }

}




const finishButton = document.getElementById('finish-button');

finishButton.addEventListener('click', closeResults);

function closeResults() {
    location.href = "homedataprovider";
}

