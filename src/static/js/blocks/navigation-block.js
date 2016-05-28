import $ from 'jquery';

// This ensures that navigation blocks which contain checkboxes get the correct tags applied

export const init = () => {
  $('.navigation-block__link input[type="radio"]:checked').closest(
    '.navigation-block__link').addClass('navigation-block__link--active');

  $('.navigation-block__link input[type="radio"]').change(function initNavigationBlock() {
    const $this = $(this);
    const name = $this.attr('name');

    $(`input[type="radio"][name="${name}]`).closest(
      '.navigation-block__link').removeClass('navigation-block__link--active');
    $(`input[type="radio"][name="${name}"]:checked`).closest(
      '.navigation-block__link').addClass('navigation-block__link--active');
  });
};
