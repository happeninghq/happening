import $ from 'jquery';

export const init = () => {
  $('.appearance').each(function initAppearance() {
    const $this = $(this);
    const customCss = $this.find('#customCSS');
    $this.find('input[type="color"]').keyup(() => {
      customCss.html(':root {');
      $('input[type="color"]').each(function initColourPicker() {
        const $$this = $(this);
        customCss.append(`--${$$this.attr('name')}: ${$$this.val()};`);
      });
      customCss.append('}');
    });
  });
};
