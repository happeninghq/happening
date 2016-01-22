$(function() {
    $('.properties-widget').each(function() {
        function property(name, type) {
            return {
                name: ko.observable(name),
                type: ko.observable(type),
                deleteProperty: function() {
                    viewModel.properties.remove(this);
                }
            }
        }

        var viewModel = {
            properties: ko.observableArray(),
            addProperty: function() {
                viewModel.properties.push(property());
            }
        }

        viewModel.value = ko.computed(function() {
            // Convert viewModel.properties into json
            return JSON.stringify(ko.toJS(viewModel).properties);
        });

        var $this = $(this);

        $this.data('reload', function() {
            var value = $this.find('[type="hidden"]').val();
            viewModel.properties.removeAll();
            if (value) {
                value = JSON.parse(value);
                for (var i in value) {
                    viewModel.properties.push(property(value[i].name, value[i].type));
                }
            }
        });


        $this.data('reload')();
        ko.applyBindings(viewModel, this);
    });
});