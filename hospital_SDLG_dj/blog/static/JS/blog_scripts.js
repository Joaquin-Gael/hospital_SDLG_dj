document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const navbar = document.getElementById('navbar');

    menuToggle.addEventListener('click', function() {
        navbar.classList.toggle('hidden');
        navbar.classList.toggle('flex');
    });
});
