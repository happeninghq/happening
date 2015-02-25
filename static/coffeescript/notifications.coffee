$ ->
  notifications_loaded = false
  $("#notifications").click ->
    if not notifications_loaded
      notifications = $(this)
      $.ajax("/notifications/short").complete (response) ->
        $('#notification-dropdown-content').html response.responseText
        notifications_loaded = true
        notifications.find(".dropdown").show()
      false

  $('#notifications li').click ->
    window.location = $(this).data('url')
    false