import $ from 'jquery';

export const init = () => {
  // Address widgets will reload properly
  // but there is no hidden input - so instead we add a data-val method
  $('.address-widget').each(function initAddressWidget() {
    const $this = $(this);

    $this.data('val', (v) => {
      for (const k in v) {
        $this.find(`[name="${$this.data('name')}_${k}"]`).val(v[k]);
      }
    });
  });
};
