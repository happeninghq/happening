import $ from 'jquery';

require('jquery-datetimepicker/jquery.datetimepicker.css');

export const init = () => {
  $('.date-widget').each(function initDateWidget() {
    const $this = $(this);
    $this.datetimepicker({ timepicker: false, format: $this.data('date-format') });
  });
};
