// Allow lists to be searched and filtered

import $ from 'jquery';

function deg2rad(deg) {
  return deg * (Math.PI / 180);
}

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
  const R = 6371; // Radius of the earth in km
  const dLat = deg2rad(lat2 - lat1);
  const dLon = deg2rad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2)
    ;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const d = R * c; // Distance in km
  return d;
}

function getDistanceFromLatLonInMiles(lat1, lon1, lat2, lon2) {
  return getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) * 0.621371;
}

export const init = () => {
  $('.searchable-list').each(function searchableList() {
    let searches = [];
    let optionFilters = {};
    let locationFilters = {};

    const isVisible = (item) => {
      let searchString = '';

      if (searches.length > 0) {
        // We loop through all data attributes starting with "searchable-" and
        // build a single string
        const itemData = item.data();

        for (const attr in itemData) {
          searchString += `${itemData[attr]} `;
        }
      }

      for (const s in searches) {
        var search = searches[s];
        if (search !== '' && searchString.search(new RegExp(search, "i")) == -1) {
          // If this doesn't match, we return false
          return false;
        }
      }

      for (const optionFilter in optionFilters) {
        const d = item.data(`searchable-${optionFilter}`);
        if (!d || d.search(new RegExp(optionFilters[optionFilter].join("|"), "i")) == -1) {
          return false;
        }
      }

      for (const locationFilter in locationFilters) {
        if (locationFilters[locationFilter][0]) {
          const [searchLatitude, searchLongitude] = locationFilters[locationFilter][0].split(',');
          const distance = parseInt(locationFilters[locationFilter][1], 10);

          if (isNaN(distance)) {
            continue;
          }

          // Only search if a location is defined
          const d = item.data(`searchable-${locationFilter}`);
          if (!d) {
            return false;
          }

          const [latitude, longitude] = d.split(',');

          const dd = getDistanceFromLatLonInMiles(searchLatitude, searchLongitude,
                                           latitude, longitude);

          if (dd > distance) {
            return false;
          }
        }
      }

      return true;
    };

    const $this = $(this);
    $this.data('searchable-list', {
      clearFilters: () => {
        searches = [];
        optionFilters = {};
        locationFilters = {};
      },

      search: (content) => {
        searches.push(content);
      },

      optionFilter: (field, options) => {
        optionFilters[field] = options;
      },

      locationFilter: (field, location, distance) => {
        locationFilters[field] = [location, distance];
      },

      draw: () => {
        $this.find('.searchable-list__item').each(function searchableListItem() {
          const $$this = $(this);
          if (isVisible($$this)) {
            $$this.removeClass('searchable-list__item--filtered');
          } else {
            $$this.addClass('searchable-list__item--filtered');
          }
        });
      },
    });
  });
};
