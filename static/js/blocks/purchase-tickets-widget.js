/**
 * Used when purchasing tickets
 */
$(function() {
    $('.purchase-tickets-widget').each(function() {
        $this = $(this);

        var total_field = $this.find('.tickets__totals__total');

        var selects = $this.find('select');
        var btn = $this.find('button');


        function update_total() {
            var total_tickets = 0;
            var total_cost = 0;

            selects.each(function() {
                var number_of_tickets = $(this).val();
                total_tickets += number_of_tickets;
                total_cost += $(this).parents('tr').data('price') * number_of_tickets;
            });
            
            total_field.text('£' + (total_cost / 100) + ' Total');
            

            if (total_tickets == 0) {
                btn.attr('disabled', 'disabled');
            } else {
                btn.removeAttr('disabled');
            }
        };

        selects.change(update_total);

        update_total();
    });
});