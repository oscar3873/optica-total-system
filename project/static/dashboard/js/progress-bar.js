document.addEventListener('DOMContentLoaded', () => {
    const employeeProgressBar = document.getElementById('employee-progress-bar');
    let progress = employeeProgressBar.getAttribute('data-progress');
    let objetive = employeeProgressBar.getAttribute('data-objetive');
    let percent = parseInt((progress*100)/objetive);
    employeeProgressBar.style.width = `${percent}%`
    employeeProgressBar.innerHTML = `${percent}%`
});