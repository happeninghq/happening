/**
 * Enable data-tables on all tables with a class of "data-table"
 */
$(function() {
    $(".data-table").each(function() {
        $this = $(this);
        $this.data('setup-datatable', function() {
            $this.DataTable({
                "dom": 'rtip'
            });
        });

        $this.data('destroy-datatable', function() {
            $this.dataTable().fnDestroy();
        });

        $this.data('refresh-datatable', function() {
            $this.data('destroy-datatable')();
            $this.data('setup-datatable')();
        });

        $this.data('setup-datatable')();
    });
});