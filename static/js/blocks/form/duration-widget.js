$(function() {
    $('.duration-widget').each(function() {

        var viewModel = {
            days: ko.observable(0),
            hours: ko.observable(0),
            minutes: ko.observable(0),
            seconds: ko.observable(0)
        }

        viewModel.value = ko.computed(function() {
            // Convert viewModel.properties into int
            return (parseInt(viewModel.days()) * 86400) + (parseInt(viewModel.hours()) * 3600) + (parseInt(viewModel.minutes()) * 60) + parseInt(viewModel.seconds());
        });

        $this = $(this);

        $this.data('reload', function() {
            var value = $this.find('[type="hidden"]').val();

            var days = Math.floor(value / 86400);
            value -= days * 86400;

            var hours = Math.floor(value / 3600) % 24;
            value -= hours * 3600;

            var minutes = Math.floor(value / 60) % 60
            value -= minutes * 60

            viewModel.days(days);
            viewModel.hours(hours);
            viewModel.minutes(minutes);
            viewModel.seconds(value);
        });


        $this.data('reload')();
        ko.applyBindings(viewModel, this);
    });
});