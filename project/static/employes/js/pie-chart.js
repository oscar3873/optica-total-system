document.addEventListener('DOMContentLoaded', () => {

  //                                                PARA OBJETIVOS DE SUCURSAL
  if(document.getElementById('branch-progress') != null){
    const branchProgressValue = parseInt(document.getElementById('branch-progress').textContent);
  const branchObjetiveValue = parseInt(document.getElementById('branch-objetive').textContent);
  const percentBranchProgress = (branchProgressValue*100)/branchObjetiveValue;

  const pieMonthObjetiveData = {
    labels: [
      "Progreso",
      "Faltante",
    ],
    datasets: [{
      data: [ `${percentBranchProgress.toFixed(1)}`, `${100-percentBranchProgress.toFixed(1)}` ],
      backgroundColor: [
        "#2c7be5",
        "#232e3c",
      ],
      hoverOffset: 4,
    }],
  };

  var pieCtx = monthObjetive.getContext('2d');

  var myPieChart = new Chart(pieCtx, {
    /* IMPORTANTE: cargamos el complemento */
    plugins: [ChartDataLabels],
    type: 'pie',
    data: pieMonthObjetiveData,
    options: {
      plugins: {
        datalabels: {
          /* anchor puede ser "start", "center" o "end" */
          anchor: "center",
          /* Podemos modificar el texto a mostrar */
          formatter: (dato) => dato + "%",
          /* Color del texto */
          color: "white",
          /* Formato de la fuente */
          font: {
            family: '"Poppins", Times, serif',
            size: "20",
            weight: "400",
          },
        }
      }
    }
  });
  }
  


  //                                                PARA OBJETIVOS DE EMPLEADO

  if(document.getElementById('employee-progress') != null){
    const employeeProgress = document.getElementById('employee-progress');
    const employeeProgressValue = parseInt(employeeProgress.textContent);
    const employeeObjetiveValue = parseInt(document.getElementById('employee-objetive').textContent);
    const percentEmployeeProgress = (employeeProgressValue*100)/employeeObjetiveValue;
    

    let pieData;
    if(percentEmployeeProgress<=(100-percentEmployeeProgress)){
      pieData = {
        labels: [
          "Progreso",
          "Faltante",
        ],
        datasets: [{
            data: [ `${percentEmployeeProgress.toFixed(1)}`, `${100-percentEmployeeProgress.toFixed(1)}` ],
          backgroundColor: [
            "#2c7be5",
            "#232e3c",
          ],
          hoverOffset: 4,
        }],
      };
    }
    else{
      pieData = {
        labels: [
          "Progreso",
          "Faltante",
        ],
        datasets: [{
            data: [ `${percentEmployeeProgress.toFixed(1)}`, 0 ],
          backgroundColor: [
            "#2c7be5",
            "#232e3c",
          ],
          hoverOffset: 4,
        }],
      };
    }
    
  
    var pieCtx = myPieGraph.getContext('2d');
  
    var myPieChart = new Chart(pieCtx, {
      /* IMPORTANTE: cargamos el complemento */
      plugins: [ChartDataLabels],
      type: 'pie',
      data: pieData,
      options: {
        plugins: {
          datalabels: {
            /* anchor puede ser "start", "center" o "end" */
            anchor: "center",
            /* Podemos modificar el texto a mostrar */
            formatter: (dato) => dato + "%",
            /* Color del texto */
            color: "white",
            /* Formato de la fuente */
            font: {
              family: '"Poppins", Times, serif',
              size: "20",
              weight: "400",
            },
          },
          legend: {
            labels: {
                color: '#5e6e82'  // Cambia el color de la letra de las etiquetas
            }
          }
        }
      }
    });
  }
  


});








// var ctx = document.getElementById('monthObjetive').getContext('2d');
    
//     // Define los datos del gráfico de torta con porcentajes
//     var datosTorta = {
//         labels: ['Faltante (25%)', 'Progreso (75%)'],
//         datasets: [{
//             data: [25,75], //la suma total debe ser 100
//             backgroundColor: ["#0b1727", "#2c7be5",],
//             hoverOffset: 4
//         }]
//     };

//     // Configura las opciones del gráfico
//     var opcionesTorta = {
//         responsive: true,
//         maintainAspectRatio: false,
//     };
    
//         // Crea el gráfico de torta
//         var miGraficoTorta = new Chart(ctx, {
//             type: 'pie',
//             data: datosTorta,
//             options: opcionesTorta
//         });






