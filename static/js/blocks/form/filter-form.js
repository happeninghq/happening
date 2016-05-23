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

    // Redraw results
    searchableList.draw();

    return false;
  }

  function resetFilter() {
    form[0].reset();
    filter();
    return false;
  }


  return {
    filter,
    resetFilter,
  };
}

export const init = () => {
  $('.filter-form').each(function initFilterForm() {
    const $this = $(this);
    const filter = $($this.data('filter'));

    let f = null;
    if (filter.hasClass('data-table')) {
      f = bindFilterToDataTable($this, filter.dataTable());
    } else if (filter.hasClass('searchable-list')) {
      f = bindFilterToSearchableList($this, filter.data('searchable-list'));
    }

    $this.find('input').keyup(f.filter);
    $this.find('input').change(f.filter);

    $this.find('.filter-form__reset').click(f.resetFilter);
  });
};
