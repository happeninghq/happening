$ ->
  csrftoken = $.cookie('csrftoken')
  $('body').on 'click', '.confirm', ->
    if confirm($(this).data('confirm'))
      $('<form action=' + $(this).attr('href') + ' method="POST"><input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '"></form>').submit()
    false