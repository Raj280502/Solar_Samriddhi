document.addEventListener('DOMContentLoaded', function() {
    // Data for services and testimonials
    const services = [
        { title: "Solar Panel Installation", description: "Expert installation of high-efficiency solar panels." },
        { title: "Maintenance Services", description: "Regular maintenance to ensure optimal performance." },
        { title: "Energy Consulting", description: "Customized energy solutions to maximize savings." }
    ];

    const testimonials = [
        { name: "John Doe", feedback: "Excellent service and support throughout the installation process." },
        { name: "Jane Smith", feedback: "Highly recommend SolarPower for their professionalism and expertise." },
        { name: "Mark Johnson", feedback: "Great experience from start to finish. Very happy with the results." }
    ];

    // Populate Services
    const serviceContainer = document.getElementById('dynamic-services');
    services.forEach(service => {
        const serviceCard = document.createElement('div');
        serviceCard.classList.add('service-card');
        serviceCard.innerHTML = `<div class="service-card-content"><h3>${service.title}</h3><p>${service.description}</p></div>`;
        serviceContainer.appendChild(serviceCard);
    });

    // Populate Testimonials
    const testimonialSlider = document.getElementById('testimonial-slider');
    testimonials.forEach(testimonial => {
        const testimonialCard = document.createElement('div');
        testimonialCard.classList.add('testimonial-card');
        testimonialCard.innerHTML = `<p>"${testimonial.feedback}"</p><p>- ${testimonial.name}</p>`;
        testimonialSlider.appendChild(testimonialCard);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetElement = document.querySelector(this.getAttribute('href'));
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Change header background on scroll
    window.addEventListener('scroll', function() {
        const header = document.querySelector('header');
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
});
