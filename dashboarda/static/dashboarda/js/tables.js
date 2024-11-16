function initDataTable(tableId) {
    $('#' + tableId).DataTable({
        "order": [[0, "asc"]],
        "paging": true,
        "select": true,
        "lengthChange": true,
        "lengthMenu": [10, 25, 50, "All"],
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": true,
        "responsive": true,
        "language": {
            "emptyTable": "No hay datos disponibles en la tabla",
            "info": "Showing _START_ to _END_ of _TOTAL_ entries",
            "infoEmpty": "Mostrando 0 a 0 de 0 registros",
            "infoFiltered": "(filtered from _MAX_ total entries)",
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
});