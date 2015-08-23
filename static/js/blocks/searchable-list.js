// Allow lists to be searched and filtered
$(function() {
    $('.searchable-list').each(function() {

        var searches = [];
        var option_filters = {};


        function isVisible(item) {

            if (searches.length > 0) {
                // We loop through all data attributes starting with "searchable-" and
                // build a single string

                var searchString = "";
                var item_data = item.data();

                for (var attr in item_data) {
                    searchString += item_data[attr] + " ";
                }
            }

            for (s in searches) {
                var search = searches[s];
                if (search != "" && searchString.search(new RegExp(search, "i")) == -1) {
                    // If this doesn't match, we return false
                    return false;
                }
            }

            for (option_filter in option_filters) {
                var d = item.data("searchable-" + option_filter);
                if (!d || d.search(new RegExp(option_filters[option_filter].join("|"), "i")) == -1) {
                    return false;
                }
            }

            return true;
        }

        var $this = $(this);
        $this.data('searchable-list', {
            "clearFilters": function() {
                searches = [];
                option_filters = {};
            },

            "search": function(content) {
                searches.push(content);
            },

            "option_filter": function(field, options) {
                option_filters[field] = options;
            },

            "draw": function() {
                $this.find('.searchable-list__item').each(function() {
                    $$this = $(this);
                    if (isVisible($$this)) {
                        $$this.removeClass('searchable-list__item--filtered');
                    } else {
                        $$this.addClass('searchable-list__item--filtered');
                    }
                });
            }
        });
    });
});