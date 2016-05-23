// Allow lists to be searched and filtered

import $ from 'jquery';

export const init = () => {
  $(() => {
    $('.searchable-list').each(function searchableList() {
      let searches = [];
      let optionFilters = {};

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

        return true;
      };

      const $this = $(this);
      $this.data('searchable-list', {
        clearFilters: () => {
          searches = [];
          optionFilters = {};
        },

        search: (content) => {
          searches.push(content);
        },

        optionFilter: (field, options) => {
          optionFilters[field] = options;
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
  });
};
