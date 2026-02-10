const onboardingBtn = document.querySelector(".primary-hover-btn");
const onboardingContainer = document.querySelector(".onboarding-container");
const onboardingOverlay = document.querySelector(".onboarding-overlay");
const skipBtn = document.querySelector(".onboarding-container .onboarding-skip-btn");
const steps = document.querySelectorAll(".onboarding-container .onboarding-step");
const stepsContainer = document.querySelector(".onboarding-container .onboarding-steps");
const nextBtn = document.querySelector(".onboarding-container .onboarding-next-btn");
const dots = document.querySelectorAll(".onboarding-container .onboaring-dot");

let stepPosition = 0;
let currentStep = 0;

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

  if (currentStep == steps.length - 1) {
    nextBtn.innerHTML = "Finish";
  }
});