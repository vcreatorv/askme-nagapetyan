document.addEventListener('DOMContentLoaded', function() {
    const tags = document.querySelectorAll('.tag-badge');
    const colors = ['text-bg-secondary', 'text-bg-primary', 'text-bg-success', 'text-bg-danger', 'text-bg-warning', 'text-bg-info', 'text-bg-dark'];

    tags.forEach(tag => {
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        tag.classList.add(randomColor);
    });
});
