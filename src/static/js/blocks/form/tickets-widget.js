import $ from 'jquery';
import ko from 'knockout';

export const init = () => {
  $('.tickets-widget').each(function initTicketsWidget() {
    function ticket(name, number, price,
                    visible, restrictionEnabled,
                    restrictionFilter, waitingListEnabled, pk) {
      return {
        pk: ko.observable(pk),
        name: ko.observable(name),
        number: ko.observable(number),
        price: ko.observable(price),
        visible: ko.observable(visible),
        waiting_list_enabled: ko.observable(waitingListEnabled),
        restriction_enabled: ko.observable(restrictionEnabled),
        restriction_filter: ko.observable(restrictionFilter),
        deleteTicket() {
          viewModel.tickets.remove(this);
        },
      };
    }

    const viewModel = {
      mode: ko.observable('add_remove'),
      current_ticket: ko.observable(),
      editing_restriction_filter: ko.observable(),
      tickets: ko.observableArray(),
      addTicket() {
        viewModel.tickets.push(ticket('', 0, 0, true, false, '', false));
      },
      editRestrictionFilter(editTicket) {
        viewModel.current_ticket(editTicket);
        viewModel.editing_restriction_filter(editTicket.restriction_filter());
        viewModel.mode('edit_restriction_filter');
      },
      confirmRestrictionFilter() {
        viewModel.current_ticket().restriction_filter(viewModel.editing_restriction_filter());
        viewModel.mode('add_remove');
      },
    };

    viewModel.value = ko.computed(() =>
      // Convert viewModel.tickets into json
      JSON.stringify(ko.toJS(viewModel).tickets)
    );

    const $this = $(this);

    $this.data('reload', () => {
      const value = $this.find('[type="hidden"]').val();

      viewModel.tickets.removeAll();
      if (value) {
        const decodedValue = JSON.parse(value);
        for (const i in decodedValue) {
          viewModel.tickets.push(ticket(
            decodedValue[i].name,
            decodedValue[i].number,
            decodedValue[i].price,
            decodedValue[i].visible,
            decodedValue[i].restriction_enabled,
            decodedValue[i].restriction_filter,
            decodedValue[i].waiting_list_enabled,
            decodedValue[i].pk));
        }
      }
    });

    $this.data('reload')();

    ko.applyBindings(viewModel, this);
  });
};
