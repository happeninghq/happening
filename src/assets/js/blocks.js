import * as blocksForm from './blocks/form/form';

import * as dataTable from './blocks/data-table';
import * as navigationBlock from './blocks/navigation-block';
import * as notificationsList from './blocks/notifications-list';
import * as purchaseTicketsWidget from './blocks/purchase-tickets-widget';
import * as searchableList from './blocks/searchable-list';
import * as time from './blocks/time';
import * as dropdown from './blocks/dropdown';
import * as toggle from './blocks/toggle';

export const init = () => {
  searchableList.init();
  dataTable.init();
  blocksForm.init();
  navigationBlock.init();
  notificationsList.init();
  purchaseTicketsWidget.init();
  time.init();
  dropdown.init();
  toggle.init();
};
