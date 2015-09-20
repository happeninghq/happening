$(function() {
    $('.tickets-widget').each(function() {
        function ticket(name, number, visible, pk) {
            return {
                pk: ko.observable(pk),
                name: ko.observable(name),
                number: ko.observable(number),
                visible: ko.observable(visible),
                deleteTicket: function() {
                    viewModel.tickets.remove(this);
                }
            }
        }

        var viewModel = {
            tickets: ko.observableArray(),
            addTicket: function() {
                viewModel.tickets.push(ticket("", 0, true));
            }
        }

        viewModel.value = ko.computed(function() {
            // Convert viewModel.tickets into json
            return JSON.stringify(ko.toJS(viewModel).tickets);
        });

        $this = $(this);

        $this.data('reload', function() {
            viewModel.tickets.removeAll();
            var value = $this.find('[type="hidden"]').val();
            if (value) {
                value = JSON.parse(value);
                for (var i in value) {
                    viewModel.tickets.push(ticket(value[i].name, value[i].number, value[i].visible, value[i].pk));
                }
            }
        });

        $this.data('reload')();
        
        ko.applyBindings(viewModel, this);
    });
});