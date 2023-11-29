document.addEventListener("DOMContentLoaded", function () {
    const colorInput = document.getElementById('color-input-disabled');
    const selectElement = document.getElementById("id_label");
    
    selectElement.addEventListener("change", function () {
        let selectedId = selectElement.value;
        let options = Array.from(selectElement.getElementsByTagName("option"));

        if(selectedId != ''){
            options.forEach(option => {
                if(option.value == selectedId){
                    let textOption = option.textContent;
                    let listWords = textOption.split(' - ');
                    colorInput.value = listWords[1];
                }
            });
        }
        else{
            colorInput.value = '#000000';
        }
        
    });
});