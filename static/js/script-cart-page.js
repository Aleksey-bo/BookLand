window.addEventListener('DOMContentLoaded', () => {
  const popup = (overlayModalSelector, closeSelector) => {
    const overlayModal = document.querySelector(overlayModalSelector),
      closeBtns = overlayModal.querySelectorAll(closeSelector);

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
      });
    });

  }

  handleForm('#showPopupButton', '.overlay');
  popup('.overlay', '.btn-close');
});
