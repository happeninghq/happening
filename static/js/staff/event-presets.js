import $ from 'jquery';

export const init = () => {
  $('.event-preset').click(function initEventPreset() {
    $('form')[0].reset();
    const preset = $(this).data('preset');
    for (const k in preset) {
      if (preset.hasOwnProperty(k)) {
        let v = preset[k];

        if (Array.isArray(v)) {
          v = JSON.stringify(v);
        }

        $(`[name="${k}"],[data-name="${k}"]`).each(function() {
          if ($(this).data('val')) {
            $(this).data('val')(v);
          } else {
            $(this).val(v);
          }
        });
      }
    }

    $('.widget').each(function() {
      if ($(this).data('reload')) {
        $(this).data('reload')();
      }
    });
  });
};
