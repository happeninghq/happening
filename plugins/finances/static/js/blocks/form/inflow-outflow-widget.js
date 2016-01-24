$(function() {
    $('.inflow-outflow-widget').each(function() {
        var $this = $(this)

        var viewModel = {
            inflowI: ko.observable(),
            outflowI: ko.observable(),
        }

        viewModel.inflow = ko.computed({
            read: function() {
                if (viewModel.inflowI() == 0) {
                    return "";
                }
                return viewModel.inflowI();
            },
            write: function(v) {
                if (parseInt(v) < 0) {
                    viewModel.inflowI(0);
                    viewModel.outflow(0 - v);
                } else {
                    viewModel.outflowI(0);
                    viewModel.inflowI(v);
                }
            }
        });

        viewModel.outflow = ko.computed({
            read: function() {
                if (viewModel.outflowI() == 0) {
                    return "";
                }
                return viewModel.outflowI();
            },
            write: function(v) {
                if (parseInt(v) < 0) {
                    viewModel.outflowI(0);
                    viewModel.inflow(0 - v);
                } else {
                    viewModel.inflowI(0);
                    viewModel.outflowI(v);
                }
            }
        });

        viewModel.value = ko.computed(function() {
          if (viewModel.inflowI() > 0) {
            return viewModel.inflowI() * 100;
          } else {
            return 0 - viewModel.outflowI() * 100;
          }
        });

        $this.data('reload', function() {
            value = $this.find('[type="hidden"]').val();
            if (value) {
                if (value > 0) {
                    viewModel.outflowI(0);
                    viewModel.inflowI(value / 100);
                } else {
                    viewModel.inflowI(0);
                    viewModel.outflowI(0 - value / 100);
                }
            }
        });

        $this.data('reload')();

        ko.applyBindings(viewModel, this);
    });
});