document.addEventListener("DOMContentLoaded", function () {
    const classBubbles = document.querySelectorAll(".class-bubble");
    const dragBoxes = document.querySelectorAll(".drag-box");

    classBubbles.forEach((bubble) => {
        bubble.addEventListener("dragstart", function (e) {
            e.dataTransfer.setData("text", e.target.innerHTML);
            e.target.classList.add("dragging");
        });

        bubble.addEventListener("dragend", function (e) {
            e.target.classList.remove("dragging");
        });
    });

    dragBoxes.forEach((box) => {
        box.addEventListener("dragover", function (e) {
            e.preventDefault();
            box.classList.add("drag-over");
        });

        box.addEventListener("dragleave", function (e) {
            box.classList.remove("drag-over");
        });

        box.addEventListener("drop", function (e) {
            e.preventDefault();
            const draggedElement = document.querySelector(".dragging");

            if (draggedElement) {

                const classColor = draggedElement.classList[1];
                box.style.backgroundColor = getColorForClass(classColor);
                box.innerHTML = draggedElement.innerHTML;
                box.classList.remove("drag-over");
            }
        });
    });

    function getColorForClass(className) {
        switch (className) {
            case "blue":
                return "#e2f2fd";
            case "yellow":
                return "#fff9c4";
            case "purple":
                return "#f3e5f5";
            case "green":
                return "#e8f5e9";
            case "red":
                return "#ffebee";
            default:
                return "#ffffff";
        }
    }
});
