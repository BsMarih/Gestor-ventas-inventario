document.addEventListener("DOMContentLoaded", function () {
    const categoryInput = document.querySelector("input[name='category']");
    const typeSelect = document.getElementById("type-select");
    const typeInput = document.getElementById("type-input");

    categoryInput.addEventListener("change", function () {
        typeSelect.innerHTML = '<option value="">Seleccione un tipo</option>';
        typeInput.value = "";

        if (!this.value.trim()) {
            return;
        }

        const requestedCategory = this.value.trim();
        fetch(`${getTypesUrl}?category=${encodeURIComponent(requestedCategory)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`No se pudieron cargar los tipos (${response.status})`);
                }
                return response.json();
            })
            .then(types => {
                if (categoryInput.value.trim() !== requestedCategory) {
                    return;
                }

                types.forEach(type => {
                    const option = document.createElement("option");
                    option.value = type;
                    option.textContent = type;
                    typeSelect.appendChild(option);
                });
            })
            .catch(error => console.error(error));
    });

    typeSelect.addEventListener("change", function () {
        if (this.value !== "") {
            typeInput.value = this.value;
        }
    });

    typeInput.addEventListener("input", function () {
        typeSelect.value = "";
    });
});
