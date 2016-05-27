require('../sass/main.scss');

// jQuery is required for django-debug-toolbar
// and also used in a few UI modules
import jQuery from 'jquery';
window.jQuery = jQuery;


import * as confirm from './confirm';
import * as stripe from './stripe.js';

import * as appearance from './admin/appearance';
import * as manageCheckIns from './admin/manage-check-ins';
import * as eventPresets from './staff/event-presets';

import * as blocks from './blocks.js';

document.addEventListener('DOMContentLoaded', () => {
  confirm.init();
  stripe.init();

  appearance.init();
  manageCheckIns.init();
  eventPresets.init();

  blocks.init();
});
