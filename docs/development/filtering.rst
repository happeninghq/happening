.. _dev_filtering:

Filtering
==============

Filtering is used frequently in Happening to allow viewing subsets of large amounts of data. It involves the creation of a ``filter-form`` and associating it with either a ``searchable-list`` or a :ref:`dev_datatables`::

    <form class="filter-form input-grid" data-filter="#members-table">
        <div class="input-grid__container">
            <label class="input-grid__container__item" for="search">Search</label>
            <input class="filter-form__search-filter" name="search" type="search">
        </div>
        <span class="input-grid__header">Status</span>
        <div class="input-grid__container">
            <label class="input-grid__container__item radio"><input name="member-status" type="checkbox" class="checkbox filter-form__option-filter" value="non-member">Non-member</label>
            <label class="input-grid__container__item radio"><input name="member-status" type="checkbox" class="checkbox filter-form__option-filter" value="member">Member</label>
            <label class="input-grid__container__item radio"><input name="member-status" type="checkbox" class="checkbox filter-form__option-filter" value="staff">Staff</label>
        </div>
    </form>

In this example, the filter-form applies to a datatable identified by the id ``members-table``. This could equally apply to a ``searchable-list`` as the API is identical. It has a search box used to search every field (using the class ``filter-form__search-filter``), and some checkboxes for filtering based on the ``member-status`` attribute (which would allow for filtering non-members, members, and staff members).

The available filter types are listed below.

*search-filter*

This allows for a text based search either on the whole table.

*option-filter*

This performs a search which checks that the specified column (as decided by the "name" field) matches one of the selected values. If no values are selected, no filtering is performed. To match against multiple values, separate valid values by a |. e.g::
    
    <label class="input-grid__container__item radio"><input name="age" type="checkbox" class="checkbox filter-form__option-filter" value="20|21|22|23|24|25|26|27|28|29">20-29</label>


**Searchable Lists**

Searchable Lists are collections of items which can be search/filtered by a filter-form. As an example::
    
    <div class="searchable-list" id="events-list">
        {% for event in all_events %}
            <div class="block block-list__item event-block searchable-list__item" data-searchable-title="{{event.title}}" data-searchable-description="{{event.description}}">
                <!-- ... -->
            </div>
        {% endfor %}
    </div>

The container must have the class ``searchable-list`` and each item must have the class ``searchable-list__item``. In this case, we are adding a "title", and "description" to the item, which can be filtered as mentioned above. All data added using these data-searchable-* attributes will be searched using the overal search functionality.