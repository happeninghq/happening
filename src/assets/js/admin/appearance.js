import $ from 'jquery';
import spectrum from 'spectrum-colorpicker';
require('spectrum-colorpicker/spectrum.css');

export const init = () => {
  $('.appearance').each(function initAppearance() {
    const $this = $(this);
    const customCss = $this.find('#customCSS');

    const resetCSS = () => {
      customCss.html(':root {');
      $this.find('input[type="color"]').each(function initColourPicker() {
        const $$this = $(this);
        if ($$this.data('spectrum-color')) {
          customCss.append(`--${$$this.attr('name')}: ${$$this.data('spectrum-color')};`);
          $$this.data('spectrum-color', null);
        }
        customCss.append(`--${$$this.attr('name')}: ${$$this.val()};`);
      });
      customCss.append('}');
    };

    $this.find('input[type="color"]').spectrum({
      showInput: true,
      showInitial: true,
      preferredFormat: "hex"
    }).on('move.spectrum', (e, tinycolor) => {
      const c = tinycolor.toHexString();
      $(e.target).val(c);
      $(e.target).data('spectrum-color', c);
      resetCSS();
    }).change(function onChange() {
      $(this).spectrum("set", $(this).val());
      resetCSS();
    }).click(function onClick() {
      $(this).spectrum('show');
      return false;
    });
  });
};
