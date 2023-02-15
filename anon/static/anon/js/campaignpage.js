document.getElementById("kg-button").addEventListener('click', onClickShow);
document.getElementById("close-button").addEventListener('click', onClickClose);

function onClickShow() {
    document.getElementById('kg-window').style.display = 'flex';
}

function onClickClose() {
    document.getElementById('kg-window').style.display = 'none';
}