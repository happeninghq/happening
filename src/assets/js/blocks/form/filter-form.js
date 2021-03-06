// This applies a filter to either a data-table or a searchable-list

import 'datatables';
import $ from 'jquery';

const bindFilterToDataTable = (form, datatable) => {
  function filter() {
    // Clear existing filters
    datatable.columns().search('');
    datatable.search('');

    // Find any "search" filters

    form.find('.filter-form__search-filter').each(function initSearchFilter() {
      datatable.search($(this).val());
    });

    // "Option" filters

    const optionFilters = {};

    form.find('.filter-form__option-filter').each(function initOptionFilter() {
      if ($(this).is(':checked')) {
        if (!(optionFilters.hasOwnProperty($(this).attr('name')))) {
          optionFilters[$(this).attr('name')] = [];
        }

        optionFilters[$(this).attr('name')].push($(this).attr('value'));
      }
    });

    for (const name in optionFilters) {
      datatable.column(`${name}:name`).search(optionFilters[name].join('|'), true, false);
    }

    // Redraw results
    datatable.draw();

    return false;
  }

  const resetFilter = () => {
    form[0].reset();
    filter();
    return false;
  };


  return {
    filter,
    resetFilter,
  };
}

function bindFilterToSearchableList(form, searchableList) {
  function filter() {
    // Clear existing filters
    searchableList.clearFilters();

    // Find any "search" filters

    form.find('.filter-form__search-filter').each(function initSearchFilter() {
      searchableList.search($(this).val());
    });

    // Option filters
    const optionFilters = {};

    form.find('.filter-form__option-filter').each(function initOptionFilter() {
      if ($(this).is(':checked')) {
        if (!(optionFilters.hasOwnProperty($(this).attr('name')))) {
          optionFilters[$(this).attr('name')] = [];
        }

        optionFilters[$(this).attr('name')].push($(this).attr('value'));
      }
    });

    for (const name in optionFilters) {
      searchableList.option_filter(name, optionFilters[name]);
    }

    // Location filters
    form.find('.filter-form__location-filter').each(function initLocationFilter() {
      const $this = $(this);
      searchableList.locationFilter($this.attr('name'), $this.data('location'), $this.find('.distance-input').val());
    });

    // Redraw results
    searchableList.draw();

    return false;
  }

  function resetFilter() {
    form[0].reset();
    filter();
    return false;
  }

  form.find('.filter-form__location-filter').each(function initLocationFilter() {
    const $filter = $(this);
    const $input = $filter.find('.address-input');
    const $address_locator = $filter.find('.address-locator');
    const input = $input[0];
    let locationText = '';

    const autocomplete = new google.maps.places.Autocomplete(input);

    function clearInput() {
      $input.val('');
      $filter.data('location', '');
      locationText = '';
    }

    autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (place.geometry) {
          const latitude = place.geometry.location.lat();
          const longitude = place.geometry.location.lng();

          locationText = $input.val();
          $filter.data('location', latitude + ',' + longitude);
        } else {
          clear_input();
        }
        filter();
      });

    $input.on('blur', () => {
      if ($('.pac-item:hover').length === 0) {
        if (!($input.val() === locationText)) {
          clearInput();
          filter();
        }
      }
    });

    if (!navigator.geolocation) {
      $address_locator.hide();
    }

    $address_locator.on('click', () => {

      var geocoder = new google.maps.Geocoder();
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
          geocoder.geocode({
            'latLng': latlng
          }, function (results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
              if (results[1] && results[1].geometry) {
                const latitude = results[1].geometry.location.lat();
                const longitude = results[1].geometry.location.lng();

                $input.val(results[1].formatted_address);
                locationText = results[1].formatted_address;
                $filter.data('location', latitude + ',' + longitude);
                filter();
              } else {
                alert('No results found');
              }
            } else {
              alert('Geocoder failed due to: ' + status);
            }
          });
        }, function() {
          alert('Could not find location (1)');
        });
      } else {
        // Browser doesn't support Geolocation
        alert('Could not find location (2)');
      }

    });

  });


  return {
    filter,
    resetFilter,
  };
}

export const init = () => {
  $('.filter-form').each(function initFilterForm() {
    const $this = $(this);

    const filter = $($this.data('filter'));

    const bindToF = (f) => {
      $this.find('.filter-form__search-filter').keyup(f.filter);
      $this.find('.filter-form__search-filter').change(f.filter);

      $this.find('.filter-form__option-filter').keyup(f.filter);
      $this.find('.filter-form__option-filter').change(f.filter);

      $this.find('.filter-form__location-filter .distance-input').keyup(f.filter);
      $this.find('.filter-form__location-filter .distance-input').change(f.filter);

      $this.find('.filter-form__reset').click(f.resetFilter);
    };

    if (filter.hasClass('data-table')) {
      filter[0].addEventListener('datatable-initialised', () => {
        bindToF(bindFilterToDataTable($this, filter.DataTable()));
      });
    } else if (filter.hasClass('searchable-list')) {
      bindToF(bindFilterToSearchableList($this, filter.data('searchable-list')));
    }
  });
};
