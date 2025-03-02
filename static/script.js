const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.3
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            console.log(`Element ${entry.target.id} is partially visible in the viewport!`);
        } else {
            console.log(`Element ${entry.target.id} is not leaving in the viewport!`);
        }
    });
}, observerOptions);
document.querySelectorAll('.tweet').forEach(tweet => observer.observe(tweet));
