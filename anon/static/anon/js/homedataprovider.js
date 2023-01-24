var campaigns = document.getElementsByClassName("campaign")

for(var i = 0 ; i < campaigns.length ; i++)
    campaigns[i].addEventListener('click', onClickConfirm)

function onClickConfirm() {
  document.getElementById("loader-id").style.display = "flex"
}