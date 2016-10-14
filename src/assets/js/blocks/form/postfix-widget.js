import ko from 'knockout';
import _ from 'lodash';
import $ from 'jquery';

export const init = () => {
  _.each(document.getElementsByClassName("postfix-widget"), (elem) => {
    const $elem = $(elem);
    // We add a second input field before this one
    // and put them both in a position: relative container

    const $container = $("<div></div>");
    const $postfix = $("<input type='text'></input>");

    $container.insertBefore($elem);

    $container.append($postfix);
    $container.append($elem);

    $container.css({position: "relative", height: "1em"});
    $postfix.css({position: "absolute", left: "0", color: "green"});
    $elem.css({position: "absolute", left: "0", background: "none"});

    $elem.attr('data-bind', 'textInput: val');
    $postfix.attr('data-bind', 'value: postfix');

    const postfixText = $elem.data('postfix');

    const viewModel = {
      val: ko.observable($elem.val())
    };

    viewModel.postfix = ko.computed(() => {
        if (viewModel.val() == '') {
            return '';
        }
        return viewModel.val() + postfixText;
    });

    ko.applyBindings(viewModel, $container[0]);
  });
};
