import $ from 'jquery';
import ko from 'knockout';

export const init = () => {
  $('.enableddisabled-widget').each(function initEnabledDisabledWidget() {
    const $this = $(this);

    const viewModel = {
      enabled: ko.observable($this.find('.enableddisable-widget__enabled').is(':checked')),
    };

    $this.find('.form__field').find('select, input, textarea').each(function initObservable() {
      $(this).attr('data-bind', 'attr: {disabled: enabled() == false}');
    });

    ko.applyBindings(viewModel, this);
  });
};
