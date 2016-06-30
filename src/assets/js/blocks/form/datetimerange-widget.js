import _ from 'lodash';
import ko from 'knockout';
import { showTab } from '../toggle';

export const init = () => {
  _.each(document.getElementsByClassName("datetimerange-widget"), (widget) => {

    const toggle = widget.getElementsByClassName("toggle")[0];

    const input = widget.getElementsByClassName("datetimerange__value")[0];
    let toggleValue = "once";
    let startSending = "";
    let stopSending = "";
    if (input.value != "") {
      toggleValue = "schedule";
      startSending = input.value.split("---")[0]
      stopSending = input.value.split("---")[1]
      const activeTab = toggle.getElementsByClassName("toggle__item--schedule")[0];
      showTab(toggle, activeTab);
    }

    const viewModel = {
      toggle: ko.observable(toggleValue),
      start_sending: ko.observable(startSending),
      stop_sending: ko.observable(stopSending)
    };

    viewModel.value = ko.computed(() => {
      if (viewModel.toggle() == "once" || viewModel.start_sending() == "" || viewModel.stop_sending() == "") {
        return "";
      } else {
        return viewModel.start_sending() + "---" + viewModel.stop_sending();
      }
    });

    toggle.addEventListener('changeTab', (e) => {
      if (e.detail.tab.dataset.toggle == "#schedule") {
        viewModel.toggle("schedule");
      } else {
        viewModel.toggle("once");
      }
    });

    ko.applyBindings(viewModel, widget);
  });
};
