document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("toolsPopup");
    const openBtn = document.getElementById("openToolsPopup");
    const closeBtn = document.querySelector(".close-popup");

    openBtn.addEventListener("click", () => {
        popup.style.display = "block";
    });

    closeBtn.addEventListener("click", () => {
        popup.style.display = "none";
    });

    window.addEventListener("click", (e) => {
        if (e.target == popup) {
            popup.style.display = "none";
        }
    });
});