// Seleccionamos todas las pestañas
const acc = document.querySelectorAll('.accordion');

acc.forEach((button) => {
    button.addEventListener('click', function() {
        const targetPanelId = this.getAttribute('data-target');
        const targetPanel = document.getElementById(targetPanelId);

        // Cerrar todos los paneles antes de abrir el seleccionado
        const allPanels = document.querySelectorAll('.panel');
        allPanels.forEach(panel => {
            if (panel !== targetPanel) {
                panel.classList.remove('active');
            }
        });

        // Alternamos la visibilidad del panel
        targetPanel.classList.toggle('active');
    });
});