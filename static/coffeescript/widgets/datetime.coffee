$ ->
  $('.datetime-widget').each ->
    $this = $(this)
    $this.datetimepicker({"format": $this.data('datetime-format')})
  $('.date-widget').each ->
    $this = $(this)
    $this.datetimepicker({"timepicker": false, "format": $this.data('date-format')})
  $('.time-widget').each ->
    $this = $(this)
    $this.datetimepicker({"datepicker": false, "format": $this.data('time-format')})