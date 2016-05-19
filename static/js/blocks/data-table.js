/**
 * Enable data-tables on all tables with a class of "data-table"
 */

import * as _ from 'datatables';
import $ from 'jquery';

export const init = () => {
  $(() => {
    $('.data-table').each(function () {
      const $this = $(this);

      $this.data('setup-datatable', () => {
        $this.DataTable({
          dom: 'rtip',
        });
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

