const toggleBtn = document.querySelector('.navbar__toggleBtn');
const menu = document.querySelector('.nav-links');
const search = document.querySelector('.search-form');

toggleBtn.addEventListener('click', () => {
        menu.classList.toggle('active');
        search.classList.toggle('active-search');
});