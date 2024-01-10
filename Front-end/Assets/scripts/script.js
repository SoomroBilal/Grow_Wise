// Carousel Slider
var carou_swiper = new Swiper(".carousel", {
    spaceBetween: 20,
    effect: "fade",
    loop: true,
    centeredSlides: true,
    autoplay: {
        delay: 2000
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true
    }
});

// Testimonials Slider
var swiper = new Swiper(".testimonials-slider", {
    grabCursor: true,
    spaceBetween: 30,
    autoplay: {
        delay: 2000
    },
    pagination: {
        el: ".testimonials-pagination",
        clickable: true,
        dynamicBullets: true
    },
    breakpoints: {
        767: {
            slidesPerView: 2
        }
    }
});
    // FAQ Section
    const faqs = document.querySelectorAll(".faq");
    faqs.forEach((faq) => {
        faq.addEventListener("click", () => {
            if (!faq.classList.contains("active")) {
                faqs.forEach(faq => {
                    faq.classList.remove('active');
                });
            }
            faq.classList.toggle("active");
        });
    });


