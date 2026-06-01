const columns = document.querySelectorAll(".kanban-column");
const cards = document.querySelectorAll(".kanban-card");
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute("content");

cards.forEach((card) => {
    card.addEventListener("dragstart", () => {
        card.classList.add("dragging");
    });
    card.addEventListener("dragend", () => {
        card.classList.remove("dragging");
    });
});

columns.forEach((column) => {
    column.addEventListener("dragover", (event) => {
        event.preventDefault();
        column.classList.add("drag-over");
        const dragging = document.querySelector(".dragging");
        if (dragging) {
            column.querySelector(".kanban-column-body").appendChild(dragging);
        }
    });

    column.addEventListener("dragleave", () => {
        column.classList.remove("drag-over");
    });

    column.addEventListener("drop", async () => {
        column.classList.remove("drag-over");
        const dragging = document.querySelector(".dragging");
        if (!dragging) {
            return;
        }
        const leadId = dragging.dataset.leadId;
        const status = column.dataset.status;
        try {
            await fetch(`/api/leads/${leadId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken || "",
                },
                body: JSON.stringify({ status }),
            });
        } catch (error) {
            console.error("Falha ao atualizar status", error);
        }
    });
});
