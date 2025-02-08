document.addEventListener("DOMContentLoaded", function () {
    function adjustCaption() {
        const caption = document.querySelector(".caption");

        if (window.innerWidth < 1750) {
            if (!caption.parentElement.classList.contains("fixItems")) {
                const fixItems = document.createElement("div");
                fixItems.classList.add("fixItems");

                caption.parentNode.insertBefore(fixItems, caption);
                fixItems.appendChild(caption);
            }

        } else {
            const fixItems = document.querySelector(".fixItems");
            if (fixItems) {
                const parent = fixItems.parentNode;
                while (fixItems.firstChild) {
                    parent.insertBefore(fixItems.firstChild, fixItems);
                }
                parent.removeChild(fixItems);
            }
        }
    }

    adjustCaption();
    window.addEventListener("resize", adjustCaption);
});