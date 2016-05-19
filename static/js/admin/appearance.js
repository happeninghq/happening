import $ from 'jquery';

// This is temporary - replace with a proper widget

export const init = () => {
  $('.appearance').each(function () {
    const $this = $(this);
    const customCss = $this.find('#customCSS');
    $this.find('input[type="color"]').keyup(() => {
      customCss.html(':root {');
      $('input[type="color"]').each(function () {
        const $$this = $(this);
        customCss.append(`--${$$this.attr('name')}: ${$$this.val()};`);
      });
      customCss.append('}');
    });
  });
};
