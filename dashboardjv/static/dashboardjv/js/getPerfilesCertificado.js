document.getElementById('rut').addEventListener('input', function () {
    const rut = this.value;
    const suggestionsBox = document.getElementById('suggestions');
    
    if (rut.length > 0) {
        fetch(`/juntavecinos/buscar-perfil/?rut=${rut}`)
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = '';
                
                if (data.success) {
                    suggestionsBox.style.display = 'block';
                    
                    data.data.forEach(perfil => {
                        const li = document.createElement('li');
                        li.classList.add('list-group-item', 'list-group-item-action');
                        li.textContent = `${perfil.rut}-${perfil.dv} (${perfil.nombre} ${perfil.apellido})`;
                        li.addEventListener('click', () => {
                            document.getElementById('rut').value = perfil.rut;
                            document.getElementById('dv').value = perfil.dv;
                            document.getElementById('nombre').value = perfil.nombre;
                            document.getElementById('apellido').value = perfil.apellido;
                            document.getElementById('email').value = perfil.correo_electronico;
                            document.getElementById('direccion').value = perfil.direccion;
                            suggestionsBox.style.display = 'none';
                        });
                        suggestionsBox.appendChild(li);
                    });
                } else {
                    suggestionsBox.style.display = 'block';
                    const li = document.createElement('li');
                    li.classList.add('list-group-item', 'list-group-item-danger');
                    li.textContent = 'No se encontró ningún perfil';
                    suggestionsBox.appendChild(li);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        suggestionsBox.style.display = 'none';
    }
});