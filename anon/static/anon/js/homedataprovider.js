var campaigns = document.getElementsByClassName("campaign")

for(var i = 0 ; i < campaigns.length ; i++)
    campaigns[i].addEventListener('click', showLoader)

function showLoader() {
  document.getElementById("loader-div").style.display = "flex"
}

document.getElementById("reload-page").addEventListener('click', reloadPage);

function reloadPage() {
    document.location.reload();
}