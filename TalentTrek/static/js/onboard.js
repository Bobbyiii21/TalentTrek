const onboardingBtn = document.querySelector(".primary-hover-btn");
const onboardingContainer = document.querySelector(".onboarding-container");
const onboardingOverlay = document.querySelector(".onboarding-overlay");
const skipBtn = document.querySelector(".onboarding-skip-btn");
const steps = document.querySelectorAll(".onboarding-step");
const stepsContainer = document.querySelector(".onboarding-steps");
const nextBtn = document.querySelector(".onboarding-next-btn");
const dots = document.querySelectorAll(".onboarding-dot");
const firstName = document.querySelector("#first-name");
const lastName = document.querySelector("#last-name");
const MAXNAMELEN = 31;

const recruiter_step_3_html = "";
const job_seeker_step_3_html = "";



let stepPosition = 0;
let currentStep = 0;
let currentUser = "no_selection";
let currentName = ["", ""];



const init = () => {
  stepsContainer.style.transition = "unset";
  onboardingContainer.classList.add("active");
  onboardingOverlay.classList.add("active");
  currentStep = 0;
  stepPosition = 0;
  stepsContainer.style.transform = `translateX(-${stepPosition}px)`;
  
  dots.forEach((d) => {
    d.classList.remove("active");
  });

  dots[currentStep].classList.add("active");

  nextBtn.innerHTML = "Next";
};

onboardingBtn.addEventListener("click", () => {
  init();
});

skipBtn.addEventListener("click", () => {
  onboardingContainer.classList.remove("active");
  onboardingOverlay.classList.remove("active");
});

nextBtn.addEventListener("click", () => {
  switch (currentStep) {
    case 0:
      if (userType.changeNextSteps(currentUser)) {
        break;
      } else {
        return;
      }
    case 1:
      if (saveName()) {
        break;
      } else {
        return;
      }
    default:
      break;
  }



  stepsContainer.style.transition = "all 400ms ease";
  currentStep++;

  if (currentStep >= steps.length) {
    stepsContainer.style.transition = "unset";
    onboardingContainer.classList.remove("active");
    onboardingOverlay.classList.remove("active");
    currentStep = 0;
  }

  stepPosition += steps[0].offsetWidth;

  stepsContainer.style.transform = `translateX(-${stepPosition}px)`;

  dots.forEach((d) => {
    d.classList.remove("active");
  });

  dots[currentStep].classList.add("active");
 // dots[currentStep - 1].classList.remove("active");

  if (currentStep == (steps.length - 1)) {
    nextBtn.innerHTML = "Finish";
  }
});



// Handles the first step, selecting the right user type and picking the right questions to follow
let userType = {
  default: 'no_selection',
  job_seeker: {
    step_2_h3: 'Name',
    step_2_p: 'What is your name?',
    step_3_h3: 'Resume',
    step_3_p: 'Upload your resume below.',
  },
  recruiter: {
    step_2_h3: 'Name',
    step_2_p: 'What is your name?',
    step_3_h3: 'Company',
    step_3_p: 'What company or organization do you represent?',
  },
  no_selection: {
    step_2_h3: 'DEFAULT',
    step_2_p: 'DEFAULT',
    step_3_h3: 'DEFAULT',
    step_3_p: 'DEFAULT',
  },
  changeNextSteps: function(radioInput) {
    steps[1].querySelector("h3").innerHTML = userType[radioInput].step_2_h3;
    steps[1].querySelector("p").innerHTML = userType[radioInput].step_2_p;
    steps[2].querySelector("h3").innerHTML = userType[radioInput].step_3_h3;
    steps[2].querySelector("p").innerHTML = userType[radioInput].step_3_p;
    if (radioInput == 'no_selection') {
      return false;
    }
    return true;
  }
}

document.querySelector('#job_seeker').addEventListener("click", () => {
  currentUser = "job_seeker";
  userType.changeNextSteps(currentUser);
});

document.querySelector('#recruiter').addEventListener("click", () => {
  currentUser = "recruiter";
  userType.changeNextSteps(currentUser);
});



//Handles the second steps, getting a valid first and last name
function saveName() {
  currentName = [firstName.value, lastName.value];
  //alert(currentName);
  return true;
}



