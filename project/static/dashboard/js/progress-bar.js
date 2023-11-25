document.addEventListener('DOMContentLoaded', () => {
    const ListProgressBars = document.querySelectorAll('[id^="employee-progress-bar-"]');
    const arrayProgressBars = Array.from(ListProgressBars);

    arrayProgressBars.forEach(employeeProgressBar => {
        let progress = employeeProgressBar.getAttribute('data-progress');
        let objetive = employeeProgressBar.getAttribute('data-objetive');
        let percent = parseInt((progress*100)/objetive);
        console.log(percent);
        employeeProgressBar.style.width = `${percent}%`
        employeeProgressBar
        let numId = (employeeProgressBar.id).match(/\d+/g);
        const employeeProgress = document.getElementById(`progress-percent-${numId}`);
        employeeProgress.innerText = `${percent}%`
    });

    
});