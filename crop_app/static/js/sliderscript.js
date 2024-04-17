const properties = ["nitrogen", "phosphorous", "pottasium"]

properties.forEach(element => {
    const initialSlider = document.getElementById(element)
    initialSlider.value = initialSlider.min
    const valueElement = element.concat("-slider-value")
    const initialSliderValue = document.getElementById(valueElement)
    initialSliderValue.innerHTML = initialSlider.value
});

const nitrogen_slider = document.getElementById("nitrogen");
const phosphorous_slider = document.getElementById("phosphorous");
const pottasium_slider = document.getElementById("pottasium");


const nitrogen_sliderValue = document.getElementById("nitrogen-slider-value");
const phosphorous_sliderValue = document.getElementById("phosphorous-slider-value");
const pottasium_sliderValue = document.getElementById("pottasium-slider-value");


nitrogen_slider.addEventListener("input", function () {
    var value = nitrogen_slider.value;
    nitrogen_sliderValue.innerHTML = value;
});

phosphorous_slider.addEventListener("input", function () {
    var value = phosphorous_slider.value;
    phosphorous_sliderValue.innerHTML = value;
});

pottasium_slider.addEventListener("input", function () {
    var value = pottasium_slider.value;
    pottasium_sliderValue.innerHTML = value;
});