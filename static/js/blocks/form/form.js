import * as addressWidget from './address-widget';
import * as dateWidget from './date-widget';
import * as datetimeWidget from './datetime-widget';
import * as durationWidget from './duration-widget';
import * as emailsWidget from './emails-widget';
import * as enableddisabledWidget from './enableddisabled-widget';
import * as filterForm from './filter-form';
import * as imageWidget from './image-widget';
import * as markdownWidget from './markdown-widget';
import * as propertiesWidget from './properties-widget';
import * as ticketsWidget from './tickets-widget';
import * as timeWidget from './time-widget';

export const init = () => {
  addressWidget.init();
  dateWidget.init();
  datetimeWidget.init();
  durationWidget.init();
  emailsWidget.init();
  enableddisabledWidget.init();
  filterForm.init();
  imageWidget.init();
  markdownWidget.init();
  propertiesWidget.init();
  ticketsWidget.init();
  timeWidget.init();
};
