import $ from 'jquery';

import 'jquery-datetimepicker';
require('jquery-datetimepicker/jquery.datetimepicker.css');

export const init = () => {
  $('.datetime-widget').each(function initDatetimeWidget() {
    const $this = $(this);
    $this.datetimepicker({ format: $this.data('datetime-format') });
  });
};
