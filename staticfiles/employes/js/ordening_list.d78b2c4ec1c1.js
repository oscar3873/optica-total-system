document.addEventListener("DOMContentLoaded", function() {
  // Diccionario para llevar el seguimiento del estado de ordenamiento de cada columna
  var sortingState = {};

  // Crear una copia de la lista original al cargar la página
  var originalOrder = Array.from(document.querySelectorAll('.table tbody tr')).map(function(row) {
    return row.cloneNode(true);
  });

  // Función para ordenar la tabla por una columna específica
  function sortTable(columnIndex) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.querySelector(".table");
    switching = true;

    // Obtener el ícono actual en la columna "Nombre"
    var headerCell = document.querySelectorAll('.sortable')[columnIndex];
    var icon = headerCell.querySelector('svg');

    // Actualizar el estado de ordenamiento y cambiar el ícono
    if (sortingState[columnIndex] === "asc") {
      sortingState[columnIndex] = "desc";
      icon.classList.remove("fa-sort-down");
      icon.classList.add("fa-sort-up");
    } else if (sortingState[columnIndex] === "desc") {
      sortingState[columnIndex] = "none";
      icon.classList.remove("fa-sort-up");
      icon.classList.add("fa-sort");
    } else {
      sortingState[columnIndex] = "asc";
      icon.classList.remove("fa-sort");
      icon.classList.add("fa-sort-down");
    }
    
    // Verificar si se seleccionó "ningún orden" y restaurar la lista original
    if (sortingState[columnIndex] === "none") {
      var tbody = table.querySelector("tbody");
      tbody.innerHTML = "";
      originalOrder.forEach(function(row) {
        tbody.appendChild(row.cloneNode(true));
      });
      return;
    }

    while (switching) {
      switching = false;
      rows = table.rows;
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("td")[columnIndex];
        y = rows[i + 1].getElementsByTagName("td")[columnIndex];

        var shouldReverse = sortingState[columnIndex] === "desc";
        if ((!shouldReverse && x.textContent.toLowerCase() > y.textContent.toLowerCase()) || (shouldReverse && x.textContent.toLowerCase() < y.textContent.toLowerCase())) {
          shouldSwitch = true;
          break;
        }
      }
      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
  }

  // Agregar un evento de clic a las columnas para ordenarlas
  var sortableColumns = document.querySelectorAll(".sortable");
  sortableColumns.forEach(function(column, columnIndex) {
    column.addEventListener("click", function() {
      sortTable(columnIndex);
    });
  });
});
