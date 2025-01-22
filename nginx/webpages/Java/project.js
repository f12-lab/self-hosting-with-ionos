const projectCards = document.querySelectorAll('.project-card');

projectCards.forEach((card) => {
    card.addEventListener('click', function () {
        const isActive = this.classList.contains('active');
        projectCards.forEach((otherCard) => otherCard.classList.remove('active'));
        if (!isActive) {
            this.classList.add('active');
        }
    });
});