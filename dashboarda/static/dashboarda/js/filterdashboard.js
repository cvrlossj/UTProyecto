document.addEventListener("DOMContentLoaded", function () {
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const selects = document.querySelectorAll(".filter-select");

    // Función para mostrar el indicador de carga
    function showLoading(filterType) {
        const countElement = document.getElementById(`${filterType}_juntas_count`);
        const loadingElement = document.getElementById(`loading-${filterType}`);

        countElement.style.opacity = "0.5";
        loadingElement.classList.remove("d-none");
        loadingElement.classList.add("d-flex");
    }

    // Función para ocultar el indicador de carga
    function hideLoading(filterType) {
        const countElement = document.getElementById(`${filterType}_juntas_count`);
        const loadingElement = document.getElementById(`loading-${filterType}`);

        countElement.style.opacity = "1";
        loadingElement.classList.remove("d-flex");
        loadingElement.classList.add("d-none");
    }

    // Función para hacer la petición al servidor
    function fetchData(url, filterType, filterValue) {
        showLoading(filterType);

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({
                filter_type: filterType,
                filter_value: filterValue !== "Filtrar" ? filterValue : null,
            }),
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            // Actualizar el valor correspondiente basado en el tipo de filtro
            const countElement = document.getElementById(`${filterType}_juntas_count`);
            switch (filterType) {
                case "total":
                    countElement.textContent = data.total_juntas;
                    break;
                case "habilitadas":
                    countElement.textContent = data.habilitadas_juntas;
                    break;
                case "inhabilitadas":
                    countElement.textContent = data.inhabilitadas_juntas;
                    break;
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            const countElement = document.getElementById(`${filterType}_juntas_count`);
            countElement.textContent = "Error";
        })
        .finally(() => {
            hideLoading(filterType);
        });
    }

    // Añadir evento a cada select
    selects.forEach((select) => {
        select.addEventListener("change", function () {
            const filterType = this.dataset.filterType;
            const filterValue = this.value;

            // Si seleccionas "Filtrar", restablece los datos originales
            const url = filterValue === "Filtrar"
                ? "/superadmin/dashboard/reset_data/"
                : "/superadmin/dashboard/filter_data/";

            // Hacer la petición al servidor
            fetchData(url, filterType, filterValue);
        });
    });
});
