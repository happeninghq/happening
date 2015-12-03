/**
 * Used when purchasing tickets
 */
$(function() {
    $('.purchase-tickets-widget').each(function() {
        $this = $(this);

        var max_tickets_enabled = $this.data('max-tickets-enabled');
        var ticket_types = $this.data('active-tickets');
        var max_tickets = $this.data('max-tickets');
        var already_purchased = $this.data('already-purchased');

        if (!max_tickets_enabled) {
            max_tickets = 9999999;
            already_purchased = 0;
        }

        function create_ticket_type(data) {
            var ticket_type = {
                name: ko.observable(data.name),
                remaining_tickets: ko.observable(data.remaining_tickets),
                price: ko.observable(data.price),
                pk: ko.observable(data.pk),
                remaining_tickets_formatted: function() {
                    if (this.remaining_tickets() == 0) {
                        return "Sold Out";
                    } else if (this.remaining_tickets() == 1) {
                        return "1 Ticket";
                    } else {
                        return this.remaining_tickets() + " Tickets";
                    }
                },

                // The number of tickets I want to purchase
                purchasing_tickets: ko.observable(0),
            }

            ticket_type.price_formatted = function() {
                if (ticket_type.price() == 0) {
                    return "Free";
                }
                pennies = ticket_type.price() / 100.0
                pennies = pennies.toFixed(2);
                return "£" + pennies;
            };

            ticket_type.purchasable_tickets = ko.computed(function() {
                // This should return the number of tickets available to purchase
                var purchasing_other_tickets = viewModel.purchasing_tickets() - ticket_type.purchasing_tickets();
                var remaining_max_tickets = (max_tickets - already_purchased) - purchasing_other_tickets;

                return Math.min(ticket_type.remaining_tickets(), remaining_max_tickets);
            });

            ticket_type.purchasable_ticket_options = ko.computed(function() {
                return _.range(ticket_type.purchasable_tickets() + 1);
            });

            return ticket_type;
        }

        var viewModel = {
            active_tickets: ko.observableArray(),
        };

        viewModel.purchasing_tickets = ko.computed(function() {
            return _.reduce(_.map(viewModel.active_tickets(), function (t) {
                return t.purchasing_tickets();
            }), function(sum, el) {
              return sum + el
            }, 0);
        });

        viewModel.total_cost = ko.computed(function() {
            return _.reduce(_.map(viewModel.active_tickets(), function (t) {
                return t.purchasing_tickets() * t.price();
            }), function(sum, el) {
              return sum + el
            }, 0);
        });

        viewModel.total_cost_formatted = ko.computed(function() {
            pennies = viewModel.total_cost() / 100.0
            pennies = pennies.toFixed(2);
            return "£" + pennies + " Total";
        });

        _.each(ticket_types, function(t) { viewModel.active_tickets.push(create_ticket_type(t)); });

        ko.applyBindings(viewModel, this);
    });
});