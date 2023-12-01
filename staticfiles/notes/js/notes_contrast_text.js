document.addEventListener("DOMContentLoaded", function () {
    const cardList = Array.from(document.querySelectorAll('.note-card'));
    cardList.forEach(card => {
        const backgroundColor = getComputedStyle(card).backgroundColor;
        const titleElement = card.querySelector('.note-title');
        const descriptionElement = document.getElementsByClassName('note-description');

        // const textColor = getContrastYIQ(backgroundColor);
        


        const backgroundLuminance = getLuminance(backgroundColor);
        const textColor = backgroundLuminance > 0.1 ? 'black' : 'white';
        titleElement.style.color = textColor + ' !important';
    });

function getLuminance(hexcolor) {
    const r = parseInt(hexcolor.slice(1, 3), 16);
    const g = parseInt(hexcolor.slice(3, 5), 16);
    const b = parseInt(hexcolor.slice(5, 7), 16);
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255;
};

function getContrastYIQ(hexcolor) {
    const r = parseInt(hexcolor.slice(1, 3), 16);
    const g = parseInt(hexcolor.slice(3, 5), 16);
    const b = parseInt(hexcolor.slice(5, 7), 16);
    const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
    return yiq >= 128 ? 'black' : 'white';
};
    
    // const noteElement = document.querySelector('.note-card');
    // const titleElement = document.getElementsByClassName('note-title');
    // const descriptionElement = document.getElementsByClassName('note-description');
    // const textColorElement = document.querySelector('#texto');
    
    // const backgroundColor = getComputedStyle(noteElement).backgroundColor;
    // const textColor = getContrastYIQ(backgroundColor);
    // titleElement.style.color = textColor + ' !important';
    // descriptionElement.style.color = textColor + ' !important';


});
