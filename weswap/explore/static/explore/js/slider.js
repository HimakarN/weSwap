
    const slider = document.querySelector('.slider');
    let slideIndex = 0;

    function autoSlide() {
        slideIndex += 1;
        const totalSlides = slider.children.length;
        if (slideIndex >= totalSlides) {
            slideIndex = 0;
        }
        slider.scrollTo({
            left: slider.children[slideIndex].offsetLeft,
            behavior: 'smooth'
        });
    }

    setInterval(autoSlide, 3000); // Slide every 3 seconds

function scrollToSlide(slideNumber) {
    const slide = document.querySelector(`#slide-${slideNumber}`);
    if (slide) {
        slide.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',  // Adjust vertical alignment
            inline: 'start'    // Adjust horizontal alignment, if necessary
        });
    }
}