const copyButtons = document.querySelectorAll("[data-copy-target]");

copyButtons.forEach((button) => {
    button.addEventListener("click", async () => {
        const targetId = button.getAttribute("data-copy-target");
        const target = document.getElementById(targetId);
        if (!target) {
            return;
        }
        try {
            await navigator.clipboard.writeText(target.textContent.trim());
            button.textContent = "Copiado";
            setTimeout(() => {
                button.textContent = "Copiar mensagem";
            }, 1500);
        } catch (error) {
            console.error("Falha ao copiar", error);
        }
    });
});
