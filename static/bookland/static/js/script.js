window.addEventListener('DOMContentLoaded', () => {
    const select = (wrapperSelector, selectedSelector, optionsSelector) => {
        const select = document.querySelector(".select");
        const selectedOption = select.querySelector(".select__selected-option");
        const optionsList = select.querySelector(".select__options");

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

    const changeInputValue = (wrapperSelector) => {
        const wrappers = document.querySelectorAll(wrapperSelector);

        wrappers.forEach(item => {
            const decrementBtn = item.querySelector('.cart__decrement'),
                incrementBtn = item.querySelector('.cart__increment'),
                valueInput = item.querySelector('.cart__list__item__input'),
                price = item.querySelector('.cart__list__item__price span'),
                priceUnit = price.textContent;

            decrementBtn.addEventListener('click', () => {
                if (+valueInput.value <= 1) return;

                valueInput.value = --valueInput.value;
                updatePrice();
            });

            incrementBtn.addEventListener('click', () => {
                valueInput.value = ++valueInput.value;
                updatePrice();
            });

            valueInput.addEventListener('input', () => {
                updatePrice();
            });

            const updatePrice = () => {
                const inputValue = parseInt(valueInput.value);
                const itemPrice = parseFloat(priceUnit);
                if (!isNaN(inputValue) && inputValue >= 1 && !isNaN(itemPrice)) {
                    price.textContent = (inputValue * itemPrice).toFixed(2);
                } else {
                    price.textContent = itemPrice.toFixed(2);
                }
            }
        });
    }

    changeInputValue('.cart__list__item');

    const popup = (overlayModalSelector, closeSelector) => {
        const overlayModal = document.querySelector(overlayModalSelector),
            closeBtns = overlayModal.querySelectorAll(closeSelector);

        // overlayModal.style.display = "grid";

        closeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                overlayModal.style.display = "none";
            });
        });
    }

    const handleForm = (submitBtnSelector, overlayModalSelector) => {
        const submitBtn = document.querySelector(submitBtnSelector),
            overlayModal = document.querySelector(overlayModalSelector);

        submitBtn.addEventListener('click', () => {
            overlayModal.style.display = "grid";

            const fieldSelectors = ["first-name", "last-name", "country",
                "email", "phone-number", "zip-code", "delivery"];

            fieldSelectors.forEach(selector => {
                const fieldInput = document.querySelector(`#${selector}`),
                    fieldSummary = document.querySelector(`#summary-${selector}`);

                fieldSummary.textContent = fieldInput.value;
                console.log(fieldInput, fieldSummary)
            });
        });
    }

    handleForm('#showPopupButton', '.overlay');
    popup('.overlay', '.btn-close');
});