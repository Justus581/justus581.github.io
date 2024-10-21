document.addEventListener('DOMContentLoaded', () => {
    // Fetch programs from JSON
    fetch('links.json')
        .then(response => response.json())
        .then(data => {
            const programList = document.getElementById('program-list');
            data.programs.forEach(program => {
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = program.url;
                link.textContent = program.title;
                listItem.appendChild(link);
                programList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error loading JSON:', error));

    // Toggle dark mode
    const modeIcon = document.getElementById('mode-icon');
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    modeIcon.src = currentTheme === 'dark' ? 'icon/moon.png' : 'icon/sun.png';

    modeIcon.addEventListener('click', () => {
        const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        modeIcon.src = theme === 'dark' ? 'icon/moon.png' : 'icon/sun.png';
    });

    // Count visitors (Example: using localStorage to simulate visitor count)
    let visitorCount = localStorage.getItem('visitor-count') || 0;
    visitorCount++;
    localStorage.setItem('visitor-count', visitorCount);
    document.getElementById('visitor-count').textContent = visitorCount;

    // Hamburger menu toggle
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const navLinks = document.querySelector('.nav-links');

    hamburgerMenu.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
    // Smooth scroll to sections
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            targetElement.scrollIntoView({ behavior: 'smooth' });
            navLinks.classList.remove('active'); // 收回漢堡式選單
        });
    });
});
