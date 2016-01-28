$(function() {
    $('.tickets-widget').each(function() {
        function ticket(name, number, price, visible, restriction_enabled, restriction_filter, waiting_list_enabled, pk) {
            return {
                pk: ko.observable(pk),
                name: ko.observable(name),
                number: ko.observable(number),
                price: ko.observable(price),
                visible: ko.observable(visible),
                waiting_list_enabled: ko.observable(waiting_list_enabled),
                restriction_enabled: ko.observable(restriction_enabled),
                restriction_filter: ko.observable(restriction_filter),
                deleteTicket: function() {
                    viewModel.tickets.remove(this);
                }
            }
        }

        var viewModel = {
            mode: ko.observable("add_remove"),
            
            current_ticket: ko.observable(),
            editing_restriction_filter: ko.observable(),


            tickets: ko.observableArray(),
            addTicket: function() {
                viewModel.tickets.push(ticket("", 0, 0, true, false, "", false));
            },
            editRestrictionFilter: function(ticket) {
                viewModel.current_ticket(ticket);
                viewModel.editing_restriction_filter(ticket.restriction_filter());
                viewModel.mode("edit_restriction_filter");
            },
            confirmRestrictionFilter: function() {
                viewModel.current_ticket().restriction_filter(viewModel.editing_restriction_filter());
                viewModel.mode("add_remove");
            }
        }

        viewModel.value = ko.computed(function() {
            // Convert viewModel.tickets into json
            return JSON.stringify(ko.toJS(viewModel).tickets);
        });

        var $this = $(this);

        $this.data('reload', function() {
            var value = $this.find('[type="hidden"]').val();

            viewModel.tickets.removeAll();
            if (value) {
                value = JSON.parse(value);
                for (var i in value) {
                    viewModel.tickets.push(ticket(value[i].name,
                                           value[i].number,
                                           value[i].price,
                                           value[i].visible,
                                           value[i].restriction_enabled,
                                           value[i].restriction_filter,
                                           value[i].waiting_list_enabled,
                                           value[i].pk));
                }
            }
        });

        $this.data('reload')();
        
        ko.applyBindings(viewModel, this);
    });
});