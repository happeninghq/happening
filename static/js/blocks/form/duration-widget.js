import $ from 'jquery';
import ko from 'knockout';

export const init = () => {
  $('.duration-widget').each(function initDurationWidget() {
    const viewModel = {
      days: ko.observable(0),
      hours: ko.observable(0),
      minutes: ko.observable(0),
      seconds: ko.observable(0),
    };

    viewModel.value = ko.computed(() =>
      // Convert viewModel.properties into int
      parseInt(viewModel.days(), 10) * 86400) +
        (parseInt(viewModel.hours(), 10) * 3600) +
          (parseInt(viewModel.minutes(), 10) * 60) +
            parseInt(viewModel.seconds(), 10);

    const $this = $(this);

    $this.data('reload', () => {
      let value = $this.find('[type="hidden"]').val();
      const days = Math.floor(value / 86400);
      value -= days * 86400;

      const hours = Math.floor(value / 3600) % 24;
      value -= hours * 3600;

      const minutes = Math.floor(value / 60) % 60;
      value -= minutes * 60;

      viewModel.days(days);
      viewModel.hours(hours);
      viewModel.minutes(minutes);
      viewModel.seconds(value);
    });


    $this.data('reload')();
    ko.applyBindings(viewModel, this);
  });
};
