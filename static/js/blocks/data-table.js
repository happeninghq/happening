/**
 * Enable data-tables on all tables with a class of "data-table"
 */

import 'datatables';
import $ from 'jquery';

require('../../sass/lib/jquery.dataTables.scss');

export const init = () => {
  $(() => {
    $('.data-table').each(function initDataTable() {
      const $this = $(this);

      $this.data('setup-datatable', () => {
        $this.dataTable();
      });

      $this.data('destroy-datatable', () => {
        $this.dataTable().fnDestroy();
      });

      $this.data('refresh-datatable', () => {
        $this.data('destroy-datatable')();
        $this.data('setup-datatable')();
      });

      $this.data('setup-datatable')();
    });
  });
};

