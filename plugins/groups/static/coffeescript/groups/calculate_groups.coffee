pluralise = (num, singular, plural) ->
  if num == 1
    return singular
  else if not plural
    return singular + "s"
  else return plural

calculate_groups = () ->
  number_of_groups = $("#id_number_of_groups").val()
  number_of_attendees = $("#number_of_attendees").text()

  attendees_per_group = Math.floor(number_of_attendees / number_of_groups)
  remainder = number_of_attendees % number_of_groups

  if attendees_per_group == Infinity
    $("#group-breakdown").text("")
    return
  if attendees_per_group == 0
    string = ""
  else
    string = (number_of_groups - remainder) + " " + pluralise((number_of_groups - remainder), "group") + " of " + attendees_per_group + " " + pluralise(attendees_per_group, "person", "people")

  if remainder > 0
    if attendees_per_group > 0
      string += " and "
    string += remainder + " " + pluralise(remainder, "group") + " of " + (attendees_per_group + 1) + " " + pluralise((attendees_per_group + 1), "person", "people")
  
  $("#group-breakdown").text("This will result in " + string + ".")

$("#id_number_of_groups").change(calculate_groups)
$("#id_number_of_groups").keyup(calculate_groups)
calculate_groups()