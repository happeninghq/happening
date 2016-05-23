import $ from 'jquery';

import 'jquery-datetimepicker';
require('jquery-datetimepicker/jquery.datetimepicker.css');

export const init = () => {
  $('.time-widget').each(function timeWidget() {
    const $this = $(this);
    $this.datetimepicker(
        { datepicker: false, format: $this.data('time-format') }
    );
  });
};
