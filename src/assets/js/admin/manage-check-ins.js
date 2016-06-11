import $ from 'jquery';

export const init = () => {
  $('.btn.check-in').click(function initcheckIns() {
    const $this = $(this);
    $.getJSON($(this).attr('href'), (r) => {
      if ($this.text() === 'Check In') {
        $this.attr('href', $this.data('cancel-check-in-url'));
        $this.text('Cancel Check In');
      } else {
        $this.attr('href', $this.data('check-in-url'));
        $this.text('Check In');
      }

      $this.closest('tr').find('.checked-in').html(r['checked-in']);

      $('#attendees-list').data('refresh-datatable')();
    });
    return false;
  });
};
