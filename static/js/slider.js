let containerSlider = document.querySelector(".personalaty");
let createSlider = document.querySelector(".create");
let createInfoSliders = document.querySelectorAll(".create-info");
let leftSlider = document.querySelector(".personalaty .fa-chevron-left");
let rightSlider = document.querySelector(".personalaty .fa-chevron-right");

let currentIndex = 0;
const slideWidth = createInfoSliders[0].offsetWidth;

if (createInfoSliders.length > 5) {
  rightSlider.style.display = "flex";
  leftSlider.style.display = "flex";
} else {
  rightSlider.style.display = "none";
  leftSlider.style.display = "none";
}

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
