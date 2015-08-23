.. _dev_datatables:

Data Tables
==============

Data Tables are used through Happening to provide sorting, filtering, and searching on data. This uses the open source DataTables jQuery plugin.

To apply it, add the "data-tables" class to a table. This will add pagination and sorting::

    <table class="data-table" id="members-table">
        <thead>
            <tr>
                <th>Username</th>
            </tr>
        </thead>
        <tbody>
            <tr><td><a href="/member/2">Member 2</a></td></tr>
            <tr><td><a href="/member/3">Member 3</a></td></tr>
        </tbody>
    </table>

**Filtering**

The filter form should be built in the same way as detailed in :ref:`dev_filtering`. However, instead of providing data using ``data-`` attributes, the queryable data will be provided in table columns::

    <table class="data-table" id="members-table">
        <thead>
            <tr>
                <th>Username</th>
                <th data-name="age">20</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><a href="/member/2">Member 2</a>
                <td>20</td>
            </td>
            </tr>
            <!-- ... -->
        </tbody>
    </table>

In this case it would add a "name" attribute which can be filtered/searched. By adding the appropriate filter type this column could be filtered::
    
    <div class="input-grid__container">
        <label class="input-grid__container__item radio"><input name="age" type="checkbox" class="checkbox filter-form__option-filter" value="20">20</label>
        <label class="input-grid__container__item radio"><input name="age" type="checkbox" class="checkbox filter-form__option-filter" value="21">21</label>
        <label class="input-grid__container__item radio"><input name="age" type="checkbox" class="checkbox filter-form__option-filter" value="22">22</label>
    </div>

If you'd rather this field still be searchable but not be visible, you can add ``data-visible="0"`` to the column, e.g::
    
    <table class="data-table" id="members-table">
        <thead>
            <tr>
                <th>Username</th>
                <th data-name="age" data-visible="0">20</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><a href="/member/2">Member 2</a>
                <td>20</td>
            </td>
            </tr>
            <!-- ... -->
        </tbody>
    </table>