// This applies a filter to either a data-table or a searchable-list

function bindFilterToDataTable(form, datatable) {
    function filter() {
        // Clear existing filters
        datatable.columns().search("")
        datatable.search("")

        // Find any "search" filters

        form.find('.filter-form__search-filter').each(function() {
            datatable.search($(this).val());
        });

        var option_filters = {};

        form.find('.filter-form__option-filter').each(function() {
            if ($(this).is(':checked')) {
                if (!(option_filters.hasOwnProperty($(this).attr('name')))) {
                    option_filters[$(this).attr('name')] = [];
                }

                option_filters[$(this).attr('name')].push($(this).attr("value"));
            }
        });

        console.log(option_filters);
        for (var name in option_filters) {
            datatable.column(name + ":name").search(option_filters[name].join("|"), true, false);
        }

        // Redraw results
        datatable.draw();

        return false;
    }

    function reset_filter() {
        form[0].reset();
        filter();
        return false;
    }


    return {
        "filter": filter,
        "reset_filter": reset_filter
    };
}

function bindFilterToSearchableList(form, searchableList) {
    function filter() {
        // Clear existing filters
        searchableList.clearFilters();

        // Find any "search" filters

        form.find('.filter-form__search-filter').each(function() {
            searchableList.search($(this).val());
        });

        var option_filters = {};

        form.find('.filter-form__option-filter').each(function() {
            if ($(this).is(':checked')) {
                if (!(option_filters.hasOwnProperty($(this).attr('name')))) {
                    option_filters[$(this).attr('name')] = [];
                }

                option_filters[$(this).attr('name')].push($(this).attr("value"));
            }
        });

        for (var name in option_filters) {
            searchableList.option_filter(name, option_filters[name]);
        }

        // Redraw results
        searchableList.draw();

        return false;
    }

    function reset_filter() {
        form[0].reset();
        filter();
        return false;
    }


    return {
        "filter": filter,
        "reset_filter": reset_filter
    };
}

$(function() {
    $('.filter-form').each(function() {
        var $this = $(this);
        var filter = $($this.data('filter'));

        var f = null;
        if (filter.hasClass('data-table')) {
            f = bindFilterToDataTable($this, filter.DataTable());
        } else if (filter.hasClass('searchable-list')) {
            f = bindFilterToSearchableList($this, filter.data('searchable-list'));
        }

        $this.find("input").keyup(f.filter);
        $this.find("input").change(f.filter);

        $this.find('.filter-form__reset').click(f.reset_filter);
    });
});