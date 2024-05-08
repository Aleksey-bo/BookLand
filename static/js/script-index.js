window.addEventListener('DOMContentLoaded', () => {
  const statusItem = () => {
    let items = document.querySelectorAll('.books__list__item');

    items.forEach(item => {
      if (item.querySelector('span.status__delivery')) {
        item.classList.add('grayed-out');
      } else {
        item.classList.remove('grayed-out');
      }
    });

  }
  
  statusItem();
});