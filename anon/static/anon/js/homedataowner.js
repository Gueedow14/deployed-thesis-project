var progressCircle = document.getElementById('progress');
var progressValue = document.getElementById('progress-value');

var progressStartValue = 0;
var speed = 25;

var progress = setInterval( () => 
  {
    progressStartValue++;

    if(progressStartValue < 35)
      progressCircle.style.background = `conic-gradient(red ${progressStartValue * 3.6}deg, white 0deg)`;
    else if (progressStartValue >= 35 & progressStartValue < 75)
      progressCircle.style.background = `conic-gradient(#ffcc00 ${progressStartValue * 3.6}deg, white 0deg)`;
    else
      progressCircle.style.background = `conic-gradient(green ${progressStartValue * 3.6}deg, white 0deg)`;


    if(progressStartValue == progressEndValue) {
      if(progressEndValue < 35) {
        progressValue.innerHTML = "Your security level is: Low";
        progressCircle.style.background = `conic-gradient(red ${progressStartValue * 3.6}deg, #ededed 0deg)`;
      } else if (progressEndValue >= 35 & progressEndValue < 75) {
        progressValue.innerHTML = "Your security level is: Mid";
        progressCircle.style.background = `conic-gradient(#ffcc00 ${progressStartValue * 3.6}deg, #ededed 0deg)`;
      } else {
        progressValue.innerHTML = "Your security level is: High";
        progressCircle.style.background = `conic-gradient(green ${progressStartValue * 3.6}deg, #ededed 0deg)`;
      }
      clearInterval(progress);
    }
  } , speed );

 
var profileButton = document.getElementById('profile-button');
var profileText = document.getElementById('profile-text');

profileButton.addEventListener('mouseover', overButton);
profileButton.addEventListener('mouseleave', leaveButton);

function overButton() {
  profileText.style.display = "block";
}

function leaveButton() {
  profileText.style.display = "none";
}
