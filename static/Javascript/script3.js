document.addEventListener('DOMContentLoaded', function() {
    const options = document.querySelectorAll('.rooftop-option');
    
    options.forEach(option => {
        option.addEventListener('click', function() {
            options.forEach(opt => opt.classList.remove('selected'));
            option.classList.add('selected');
        });
    });
});
