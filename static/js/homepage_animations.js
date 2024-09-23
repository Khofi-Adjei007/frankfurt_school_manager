
document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.animate-fadeInRight');
    cards.forEach((card, index) => {
      setTimeout(() => {
        card.classList.remove('opacity-0');  // Remove opacity-0 to trigger the fade-in
      }, index * 300);  // Stagger each card by 300ms
    });
  });
  