function initDataTable(tableId) {
    $('#' + tableId).DataTable({
        "order": [[0, "desc"]],
        "paging": true,
        "select": true,
        "lengthChange": true,
        "lengthMenu": [10, 25, 50, "All"],
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,
        "language": {
            "emptyTable": "No hay datos disponibles en la tabla",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ registros",
            "infoEmpty": "Mostrando 0 a 0 de 0 registros",
            "infoFiltered": "(filtrado de _MAX_ registros totales)",
            "lengthMenu": "Mostrar _MENU_ registros",
            "search": "Buscar:",
            "zeroRecords": "No se encontraron registros coincidentes",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            }
        }
    });
}


$(document).ready(function() {
    initDataTable('logsTableJuntaVecinos');
    initDataTable('logsTablePerfilesJunta'); 
    initDataTable('logsTablePerfiles'); 
    initDataTable('logsTableVecinos'); 
});
