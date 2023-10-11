document.addEventListener("DOMContentLoaded", () => {
    const searchContainer = document.getElementById('search-contains');

    const searchInput = document.getElementById('search_term');
    const findResults = document.getElementById("search-results");
    const percentageContainer = document.getElementById('id_percentage');
    const selectedItemsList = []; 

    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value;
        const url_search = searchContainer.getAttribute('data-url');

        if (searchTerm === "") {
            findResults.innerHTML = "";
            return;
        }

        $.ajax({
            url: url_search,
            data: {
                search_term: searchTerm,
            },
            success: function (data) {
                findResults.innerHTML = "";
                data.forEach(function (result) {
                    var checkBtn = document.createElement("input");
                    checkBtn.type = "checkbox";
                    checkBtn.data = `${result.name}`;
                    checkBtn.value = result.id;
                    checkBtn.name = result.form_name;

                    const isSelected = selectedItemsList.some(item => item.data === checkBtn.data);
                    checkBtn.checked = isSelected;

                    checkBtn.addEventListener('change', (event) => {
                        const check = event.target;
                        if (check.checked) {
                            selectedItemsList.push(check);
                            updateSelectedItemsList();
                            percentageContainer.disabled = false;
                        } else {
                            const selectedIndex = selectedItemsList.findIndex(item => item.data === check.data);
                            if (selectedIndex !== -1) {
                                selectedItemsList.splice(selectedIndex, 1);
                                updateSelectedItemsList();
                            }

                            const checkboxesInResults = document.querySelectorAll('#search-results input[type="checkbox"]');
                            checkboxesInResults.forEach((checkbox) => {
                                if (checkbox.data === check.data) {
                                    checkbox.checked = false;
                                }
                            });

                            if (selectedItemsList.length === 0) {
                                percentageContainer.disabled = true;
                                percentageContainer.value = '';
                            }
                        }
                    });

                    var label = document.createElement("label");
                    label.textContent = result.name;
                    label.htmlFor = result.name;

                    var searchResults = document.getElementById("search-results");

                    searchResults.appendChild(checkBtn);
                    searchResults.appendChild(label);
                    searchResults.appendChild(document.createElement("br"));
                });

            },
            error: function () {
                console.log(error);
            },
        });
    });

    function updateSelectedItemsList() {
        const selectedItemsContainer = document.getElementById('selected-items-list');
        selectedItemsContainer.innerHTML = ""; 

        selectedItemsList.forEach((item) => {
            const checkBtn = document.createElement('input');
            checkBtn.type = 'checkbox';
            checkBtn.checked = true; 
            checkBtn.value = item.value;
            checkBtn.data = item.data;
            checkBtn.name = item.name;

            checkBtn.addEventListener('change', (event) => {
                const check = event.target;
                if (check.checked) {
                    selectedItemsList.push(check);
                    updateSelectedItemsList();
                } else {
                    const selectedIndex = selectedItemsList.findIndex(item => item.data === check.data);
                    if (selectedIndex !== -1) {
                        selectedItemsList.splice(selectedIndex, 1);
                        updateSelectedItemsList();
                    }

                    const checkboxesInResults = document.querySelectorAll('#search-results input[type="checkbox"]');
                    checkboxesInResults.forEach((checkbox) => {
                        if (checkbox.data === check.data) {
                            checkbox.checked = false;
                        }
                    });

                    if (selectedItemsList.length === 0) {
                        percentageContainer.disabled = true;
                        percentageContainer.value = '';
                    }
                }
            });

            selectedItemsContainer.appendChild(checkBtn);

            const label = document.createElement('label');
            label.textContent = item.data;
            selectedItemsContainer.appendChild(label);
        });
    }
});
