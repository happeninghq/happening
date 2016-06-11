import $ from 'jquery';
import ko from 'knockout';

export const init = () => {
  $('.properties-widget').each(function initPropertiesWidget() {
    function property(name, type) {
      return {
        name: ko.observable(name),
        type: ko.observable(type),
        deleteProperty() {
          viewModel.properties.remove(this);
        },
      };
    }

    const viewModel = {
      properties: ko.observableArray(),
      addProperty() {
        viewModel.properties.push(property());
      },
    };

    viewModel.value = ko.computed(() =>
      // Convert viewModel.properties into json
      JSON.stringify(ko.toJS(viewModel).properties)
    );

    const $this = $(this);

    $this.data('reload',() => {
      const value = $this.find('[type="hidden"]').val();
      viewModel.properties.removeAll();
      if (value) {
        const decodedValue = JSON.parse(value);
        for (const i in decodedValue) {
          viewModel.properties.push(property(decodedValue[i].name, decodedValue[i].type));
        }
      }
    });

    $this.data('reload')();
    ko.applyBindings(viewModel, this);
  });
};
