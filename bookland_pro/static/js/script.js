window.addEventListener('DOMContentLoaded', () => {
    const select = (wrapperSelector, selectedSelector, optionsSelector) => {
        const select = document.querySelector(wrapperSelector);
        const selectedOption = select.querySelector(selectedSelector);
        const optionsList = select.querySelector(optionsSelector);

        selectedOption.addEventListener("click", function (event) {
            optionsList.style.display = optionsList.style.display === "none" ? "block" : "none";
            event.stopPropagation();
        });

        document.addEventListener("click", function (event) {
            if (!select.contains(event.target)) {
                optionsList.style.display = "none";
            }
        });
    }

    select('.select', '.select__selected-option', '.select__options');
});