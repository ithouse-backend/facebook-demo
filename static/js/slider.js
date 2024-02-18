let containerSlider = document.querySelector(".personalaty");
let createSlider = document.querySelector(".create");
let createInfoSliders = document.querySelectorAll(".create-info");
let leftSlider = document.querySelector(
  ".slider_buttons_home .fa-chevron-left"
);
let rightSlider = document.querySelector(
  ".slider_buttons_home .fa-chevron-right"
);

let currentIndex = 0;
const slideWidth = createInfoSliders[0].offsetWidth;
console.log(createInfoSliders.length);

function nextSlide() {
  currentIndex++;
  if (currentIndex >= createInfoSliders.length - 3) {
    currentIndex = 0;
  }
  updateSliderPosition();
}

function prevSlide() {
  currentIndex--;
  if (currentIndex < 0) {
    currentIndex = createInfoSliders.length - 4;
  }
  updateSliderPosition();
}

function updateSliderPosition() {
  const offset = -1 * currentIndex * slideWidth;
  createSlider.style.transform = `translateX(${offset}px)`;
}

leftSlider.addEventListener("click", prevSlide);
rightSlider.addEventListener("click", nextSlide);

document.addEventListener("keydown", function (event) {
  if (event.key === "ArrowRight") {
    nextSlide();
  } else if (event.key === "ArrowLeft") {
    prevSlide();
  }
});
