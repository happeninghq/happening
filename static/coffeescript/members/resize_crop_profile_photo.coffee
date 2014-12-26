width = 0
height = 0

cropping_width = 0
cropping_height = 0

updateCoords = (c) ->
  w_proportion = cropping_width / width
  h_proportion = cropping_height / height

  x1 = c.x / w_proportion
  x2 = c.x2 / w_proportion
  y1 = c.y / h_proportion
  y2 = c.y2 / h_proportion

  w1 = c.w / w_proportion
  h1 = c.h / h_proportion
  
  $("#id_x1").val x1
  $("#id_y1").val y1
  $("#id_x2").val x2
  $("#id_y2").val y2

$ ->

  img = new Image()
  img.onload = () ->
    height = this.height
    width = this.width

    cropping_width = $("#to_be_cropped").width()
    cropping_height = $("#to_be_cropped").height()
  img.src = $('#to_be_cropped').attr('src')

  $("#to_be_cropped").Jcrop
    aspectRatio: 1
    bgColor: "rgb(235, 235, 235)"
    onSelect: updateCoords
    onChange: updateCoords
