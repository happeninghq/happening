$(function() {
    $('.enableddisabled-widget').each(function() {
        var $this = $(this);
        
        var viewModel = {
            enabled: ko.observable($this.find('.enableddisable-widget__enabled').is(':checked'))
        }

        $this.find('.form__field').find('select, input, textarea').each(function() {
            $(this).attr('data-bind', "attr: {disabled: enabled() == false}")
        });

        ko.applyBindings(viewModel, this);
    });
});