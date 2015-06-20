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

    $this = $(this)

    $this.data 'reload', () ->
      viewModel.properties.removeAll()
      value = $this.find('[type="hidden"]').val()
      if value
        value = JSON.parse(value)
        for i in value
          viewModel.properties.push(property(i.name, i.type))


    $this.data('reload')()
    ko.applyBindings(viewModel, this)
