const onboardingBtn = document.querySelector(".primary-hover-btn");
const onboardingContainer = document.querySelector(".onboarding-container");
const onboardingOverlay = document.querySelector(".onboarding-overlay");
const skipBtn = document.querySelector(".onboarding-skip-btn");
const steps = document.querySelectorAll(".onboarding-step");
const stepsContainer = document.querySelector(".onboarding-steps");
const nextBtn = document.querySelector(".onboarding-next-btn");
const dots = document.querySelectorAll(".onboarding-dot");
const headline = document.querySelector("#headline");
const resumeUpload = document.querySelector("#hidden-resume-button");
const pfpUpload = document.querySelector("#hidden-profile-pic-button");

const recruiter_step_3_html = "";
const job_seeker_step_3_html = "";
const formData = new FormData();


let stepPosition = 0;
let currentStep = 0;
let currentUser = "no_selection";
let currentHeadline = "";
let currentResume;
let currentCompany = "";
let currentPfp;



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

document.querySelector("#resume-upload").addEventListener("click", (e) => {
  if (resumeUpload) {
    resumeUpload.click();
  }
});

document.querySelector("#profile-pic").addEventListener("click", (e) => {
  if (pfpUpload) {
    pfpUpload.click();
  }
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
      if (saveHeadline()) {
        break;
      } else {
        return;
      }
    case 2:
      if (currentUser == "job_seeker") {
        saveResume();
      } else {
        saveCompany();
      }
    case 3:
      savePfp();
    default:
      break;
  }

  stepsContainer.style.transition = "all 400ms ease";
  currentStep++;

  if (currentStep >= steps.length) {
    sendData();
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

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function sendData() {
  debugger;
  formData.append('user_type', currentUser);
  formData.append('headline', currentHeadline);
  formData.append('resume', currentResume);
  formData.append('company', currentCompany);
  formData.append('pfp', currentPfp);

  debugger;
  try {
    const response = await fetch("{% url 'accounts.onboard' %}", {
      method: "POST",
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      body: formData,
    });
    //console.log(await response.json());
  } catch (e) {
    debugger;
    console.error(e);
  }
}

// Handles the first step, selecting the right user type and picking the right questions to follow
let userType = {
  default: 'no_selection',
  job_seeker: {
    step_2_h3: 'About',
    step_2_p: 'You can write about your years of experience, industry, or skills. People also talk about their achievements or previous job experiences.',
    step_3_h3: 'Resume',
    step_3_p: 'Upload your resume below.',
  },
  recruiter: {
    step_2_h3: 'About',
    step_2_p: 'You can write about your years of experience, industry, or skills. People also talk about their achievements or previous job experiences.',
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
function saveHeadline() {
  currentHeadline = headline.value;
  return true;
}

function saveCompany() {
  currentCompany = company.value;
  return true;
}

function saveResume() {
  if (resumeUpload.files.length == 0) {
    alert("No resume selected.");
  } else {
    currentResume = resumeUpload.files[0];
  }
}

function savePfp() {
  if (pfpUpload.files.length == 0) {
    alert("No picture set.");
  } else {
    currentPfp = pfpUpload.files[0];
  }
}

// Not used, could be implemented later to preview uploaded pfp
function imagePreview(file) {
  const img = document.createElement("img");
  img.classList.add("obj");
  img.file = file;
  preview.appendChild(img); // Assuming that "preview" is the div output where the content will be displayed.

  const reader = new FileReader();
  reader.onload = (e) => {
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}