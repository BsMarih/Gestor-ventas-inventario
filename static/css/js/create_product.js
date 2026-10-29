document.addEventListener("DOMContentLoaded", function () {
    const categoryInput = document.querySelector("input[name='category']");
    const typeSelect = document.getElementById("type-select");
    const typeInput = document.getElementById("type-input");

    function loadTypes(category, selectedType = "") {
        typeSelect.innerHTML = '<option value="">Seleccione un tipo</option>';

        if (!category) {
            return;
        }

        fetch(`${getTypesUrl}?category=${encodeURIComponent(category)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`No se pudieron cargar los tipos (${response.status})`);
                }
                return response.json();
            })
            .then(types => {
                if (categoryInput.value.trim() !== category) {
                    return;
                }

                types.forEach(type => {
                    const option = document.createElement("option");
                    option.value = type;
                    option.textContent = type;
                    typeSelect.appendChild(option);
                });

                if (types.includes(selectedType)) {
                    typeSelect.value = selectedType;
                }
            })
            .catch(error => console.error(error));
    }

    categoryInput.addEventListener("change", function () {
        typeInput.value = "";
        loadTypes(this.value.trim());
    });

    typeSelect.addEventListener("change", function () {
        if (this.value !== "") {
            typeInput.value = this.value;
        }
    });

    typeInput.addEventListener("input", function () {
        typeSelect.value = "";
    });

    loadTypes(categoryInput.value.trim(), typeInput.value.trim());
});
