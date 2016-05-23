import $ from 'jquery';
import ko from 'knockout';
import _ from 'underscore';

/**
 * Used when purchasing tickets
 */
export const init = () => {
  $('.purchase-tickets-widget').each(function initPurchaseTickets() {
    const $this = $(this);

    const maxTicketsEnabled = $this.data('max-tickets-enabled');
    const ticketTypes = $this.data('active-tickets');
    let maxTickets = $this.data('max-tickets');
    let alreadyPurchased = $this.data('already-purchased');

    const viewModel = {
      active_tickets: ko.observableArray(),
    };

    if (!maxTicketsEnabled) {
      maxTickets = 9999999;
      alreadyPurchased = 0;
    }

    function createTicketType(data) {
      const ticketType = {
        name: ko.observable(data.name),
        remaining_tickets: ko.observable(data.remaining_tickets),
        price: ko.observable(data.price),
        pk: ko.observable(data.pk),
        remaining_tickets_formatted() {
          if (this.remaining_tickets() === 0) {
            return 'Sold Out';
          } else if (this.remaining_tickets() === 1) {
            return '1 Ticket';
          }
          return `${this.remaining_tickets()} Tickets`;
        },

        // The number of tickets I want to purchase
        purchasing_tickets: ko.observable(0),
      };

      ticketType.price_formatted = () => {
        if (ticketType.price() === 0) {
          return 'Free';
        }
        let pennies = ticketType.price() / 100.0;
        pennies = pennies.toFixed(2);
        return `£${pennies}`;
      };

      ticketType.purchasable_tickets = ko.computed(() => {
        // This should return the number of tickets available to purchase
        const purchasingOtherTickets = viewModel.purchasing_tickets() -
          ticketType.purchasing_tickets();
        const remainingMaxTickets = (maxTickets - alreadyPurchased) - purchasingOtherTickets;

        return Math.min(ticketType.remaining_tickets(), remainingMaxTickets);
      });

      ticketType.purchasable_ticket_options = ko.computed(() =>
        _.range(ticketType.purchasable_tickets() + 1));

      return ticketType;
    }

    viewModel.purchasing_tickets = ko.computed(() =>
      _.reduce(_.map(viewModel.active_tickets(), (t) =>
        t.purchasing_tickets()
      ), (sum, el) => sum + el, 0)
    );

    viewModel.total_cost = ko.computed(() =>
      _.reduce(_.map(viewModel.active_tickets(), (t) =>
        t.purchasing_tickets() * t.price()
      ), (sum, el) => sum + el, 0)
    );

    viewModel.total_cost_formatted = ko.computed(() => {
      let pennies = viewModel.total_cost() / 100.0;
      pennies = pennies.toFixed(2);
      return `£${pennies} Total`;
    });

    _.each(ticketTypes, (t) => viewModel.active_tickets.push(createTicketType(t)));

    ko.applyBindings(viewModel, this);
  });
};
