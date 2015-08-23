/**
 * Enable data-tables on all tables with a class of "data-table"
 */
$(function() {
    $(".data-table").DataTable({
        "dom": 'rtip'
    });
});