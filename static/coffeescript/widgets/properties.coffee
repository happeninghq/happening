$ ->
  $('.properties-widget').each ->
    property = (name, type) ->
      return {
        name: ko.observable(name)
        type: ko.observable(type)
        deleteProperty: () ->
          viewModel.properties.remove(this)
      }

    viewModel =
      properties: ko.observableArray()
      addProperty: () ->
        viewModel.properties.push(property())

    viewModel.value = ko.computed () ->
      # Convert viewModel.properties into json
      return JSON.stringify(ko.toJS(viewModel).properties)

    value = $(this).data('value')
    if value
      for i in value
        viewModel.properties.push(property(i.name, i.type))

    ko.applyBindings(viewModel, this)

    window.v = viewModel