import $ from 'jquery';

export const init = () => {

  // Address widgets will reload properly
  // but there is no hidden input - so instead we add a data-val method
  $('.address-widget').each(function initAddressWidget() {

    let longitude = null;
    let latitude = null;

    const $this = $(this);
    const $input = $this.find('.address-input');
    const $extra = $this.find('.address-extra');
    const input = $input[0];
    const $field = $this.find('.address-field');

    const $tick = $this.find('.address-tick');


    const update_data = () => {
      const data = {
        title: $input.val(),
        extra: $extra.val(),
      };

      if (longitude) {
        data.longitude = longitude;
        data.latitude = latitude;
        // Show
        $tick.show();
      } else {
        // Hide
        $tick.hide();
      }
      
      $field.val(JSON.stringify(data));
    }

    if (googleMapsEnabled) {
      const autocomplete = new google.maps.places.Autocomplete(input);

      autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (place.geometry) {
          latitude = place.geometry.location.lat();
          longitude = place.geometry.location.lng();
        } else {
          longitude = null;
          latitude = null;
        }

        update_data();
      });
    }

    $input.on('keydown', () => {
      longitude = null;
      latitude = null;
      
      update_data();
    });

    $input.on('blur', () => {
      if ($('.pac-item:hover').length === 0 ) {
        if (googleMapsEnabled) {
          google.maps.event.trigger(this, 'focus');
          google.maps.event.trigger(this, 'keydown', {
              keyCode: 13
          });
        } else {
          update_data();
        }
      }
    });

    $extra.on('blur', update_data);

    $this.data('val', (v) => {
      if (v.title) {
        $input.val(v.title);


        if (v.latitude) {
          latitude = v.latitude;
          longitude = v.longitude;
        } else {
          latitude = null;
          longitude = null;
        }

        if (v.extra) {
          $extra.val(v.extra);
        } else {
          $extra.val("");
        }

      } else {
        $input.val("");
        $extra.val("");
        longitude = null;
        latitude = null;
      }

      update_data();
    });

    $this.data('val')(JSON.parse($field.val()));
  });
};
