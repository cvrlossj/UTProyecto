document.addEventListener('DOMContentLoaded', function() {
    const regionSelect = document.getElementById('region');
    const comunaSelect = document.getElementById('comuna');
    const perfilesSelect = document.getElementById('perfilesOrganizacion');

    // Inicialmente deshabilitar los selects dependientes
    comunaSelect.setAttribute('disabled', 'true');
    perfilesSelect.setAttribute('disabled', 'true');

    // Evento para cargar comunas al seleccionar una región
    regionSelect.addEventListener('change', function() {
        const regionId = this.value;
        comunaSelect.value = '';
        perfilesSelect.innerHTML = ''; // Limpiar perfiles al cambiar de región

        if (regionId) {
            fetch(`/superadmin/load-comunas/?region_id=${regionId}`)
                .then(response => response.json())
                .then(data => {
                    comunaSelect.innerHTML = '<option value="">Selecciona una comuna</option>';
                    data.forEach(comuna => {
                        const option = document.createElement('option');
                        option.value = comuna.id;
                        option.textContent = comuna.nombre;
                        comunaSelect.appendChild(option);
                    });
                    comunaSelect.removeAttribute('disabled');
                })
                .catch(error => console.error('Error al cargar comunas:', error));
        } else {
            comunaSelect.innerHTML = '<option value="">Selecciona una comuna</option>';
            comunaSelect.setAttribute('disabled', 'true');
        }
    });

    // Evento para cargar perfiles al seleccionar una comuna
    comunaSelect.addEventListener('change', function() {
        const comunaId = this.value;
        perfilesSelect.innerHTML = ''; // Limpiar perfiles anteriores

        if (comunaId) {
            fetch(`/superadmin/get_perfiles_by_comuna/${comunaId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        data.forEach(perfil => {
                            const option = document.createElement('option');
                            option.value = perfil.rut;
                            option.textContent = `${perfil.nombre} ${perfil.apellido}`;
                            perfilesSelect.appendChild(option);
                        });
                        perfilesSelect.removeAttribute('disabled');
                    } else {
                        const option = document.createElement('option');
                        option.value = 'disabled';
                        option.textContent = 'No se encuentran perfiles para esta comuna';
                        perfilesSelect.appendChild(option);
                    }
                })
                .catch(error => console.error('Error al cargar perfiles:', error));
        } else {
            perfilesSelect.setAttribute('disabled', 'true');
        }
    });

    // Agregar validación antes de enviar el formulario
    document.querySelector('form').addEventListener('submit', function(e) {
        // Remover readonly antes de enviar el formulario
        comunaSelect.removeAttribute('disabled');
        perfilesSelect.removeAttribute('disabled');
        
        // Si los campos requeridos están vacíos, prevenir el envío
        if (!comunaSelect.value) {
            e.preventDefault();
            alert('Por favor seleccione una comuna');
        }
    });
});