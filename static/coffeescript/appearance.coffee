$ ->
  $('input[type="color"]').change $.throttle 1000, (value) ->
    theme = $('#id_theme_colour').val().substring(1)
    primary = $('#id_primary_colour').val().substring(1)
    $('body').append('<link rel="stylesheet" href="/admin/appearance/css?theme_colour=' + theme + '&primary_colour=' + primary + '" type="text/css"></link>')
