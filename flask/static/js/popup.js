function showPopup(message, type) {
    const popup = document.getElementById("popup");
    popup.textContent = message;
    popup.className = "popup " + type + " show"; // mostra com animação

    // fade out após 3 segundos
    setTimeout(() => {
        popup.classList.remove("show"); // animação de saída
    }, 3000);
}