const cells = document.querySelectorAll('td.cell-none');

cells.forEach((cell) => {
  cell.addEventListener('click', (el) => {
    cell.classList.toggle('cell-selected');
  });
});
