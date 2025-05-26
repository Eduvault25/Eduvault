const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

// Toggle manually via buttons
registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});
loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// Auto-toggle based on data-default-panel attribute
window.addEventListener("DOMContentLoaded", () => {
    const defaultPanel = container.getAttribute("data-default-panel");
    if (defaultPanel === "signup") {
        container.classList.add("active");
    } else {
        container.classList.remove("active");
    }
});
