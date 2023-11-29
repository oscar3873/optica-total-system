document.addEventListener("DOMContentLoaded", function () {
    
    // Capturar todos los links de la barra lateral
    var links = document.querySelectorAll('#navbarVerticalNav a');
    // Capturar cada dropdown
    let dropdownControlPanel = document.getElementById('control-panel');
    let dropdownObjetives = document.getElementById('sales_objetives');
    let dropdownBilling = document.getElementById('sales_billing');
    let dropdownPaymentMethods = document.getElementById('payment_methods');
    let dropdownCategories = document.getElementById('products_categories');
    let dropdownPromotions = document.getElementById('products_promotions');

    links.forEach(function (link) {
        link.addEventListener('click', function (event) {
            // Evita que el enlace se comporte como un enlace normal
            //event.preventDefault();
            let clickedLinkId = link.id;
            if (link.classList.contains('dropdown-control-panel')) {
                dropdownControlPanel.classList.add('active');
                localStorage.setItem('dropdown', dropdownControlPanel.id);
            }
            else if (link.classList.contains('dropdown-sales_objetives')) {
                dropdownObjetives.classList.add('active');
                localStorage.setItem('dropdown', dropdownObjetives.id);
            } 
            else if(link.classList.contains('dropdown-sales-billing')){
                dropdownBilling.classList.add('active');
                localStorage.setItem('dropdown', dropdownBilling.id);
            }
            else if(link.classList.contains('dropdown-payment-methods')){
                dropdownPaymentMethods.classList.add('active');
                localStorage.setItem('dropdown', dropdownPaymentMethods.id);
            }
            else if(link.classList.contains('dropdown-categories')){
                dropdownCategories.classList.add('active');
                localStorage.setItem('dropdown', dropdownCategories.id);
            }
            else if(link.classList.contains('dropdown-promotions')){
                dropdownPromotions.classList.add('active');
                localStorage.setItem('dropdown', dropdownPromotions.id);
            }
            else {
                localStorage.setItem('dropdown', null);
                
                if (!link.classList.contains('active')) {
                    links.forEach(function (otherLink) {
                        otherLink.classList.remove('active');
                    });
                    // Si el link seleccionado no es un dropdown, se le agrega la clase 'active'
                    if(link != dropdownObjetives && link != dropdownBilling && link != dropdownPaymentMethods && link != dropdownCategories && link != dropdownPromotions){
                        link.classList.add('active');
                    }
                }
            }
            localStorage.setItem('clickedLink', clickedLinkId);
        });
    });


    // Al iniciar el documento, revisa el local storage en busca de los elementos que debe activar

    let idDropdownActivatedSaved = localStorage.getItem('dropdown');
    if (idDropdownActivatedSaved != 'null') {
        let dropdownActivated = document.getElementById(idDropdownActivatedSaved);
        dropdownActivated.classList.add('active');
        dropdownActivated.setAttribute('aria-expanded', 'true');
        let idLinkActiveSaved = localStorage.getItem('clickedLink');
        let clickedLink = document.getElementById(idLinkActiveSaved);
        let ulElement = clickedLink.closest('ul');
        ulElement.classList.add('show');
    }    


    let idLinkActiveSaved = localStorage.getItem('clickedLink');
    if (idLinkActiveSaved) {
        let clickedElement = document.getElementById(idLinkActiveSaved);
        if (clickedElement) {
            clickedElement.classList.add('active');
            clickedElement.scrollIntoView();
        }   
    }


    let logOut = document.getElementById('logout');
    logOut.addEventListener('click', function(){
        localStorage.removeItem('clickedLink');
        localStorage.removeItem('dropdown');
    });
});