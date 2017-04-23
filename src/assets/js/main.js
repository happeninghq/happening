require('../sass/main.scss');

// jQuery is required for django-debug-toolbar
// and also used in a few UI modules
import jQuery from 'jquery';
window.jQuery = jQuery;

import * as ajax from './ajax';

import * as confirm from './confirm';
import * as postLink from './post_link';
import * as stripe from './stripe.js';
import * as moveFromElsewhere from './move_from_elsewhere.js';

import * as appearance from './admin/appearance';
import * as manageCheckIns from './admin/manage-check-ins';
import * as eventPresets from './admin/event-presets';
import * as emails from './admin/emails.js';

import * as blocks from './blocks.js';

import * as editPage from './edit-page.js';

import * as matchHeight from './match-height.js';

document.addEventListener('DOMContentLoaded', () => {
  ajax.init();
  confirm.init();
  postLink.init();
  stripe.init();
  moveFromElsewhere.init();

  appearance.init();
  manageCheckIns.init();
  eventPresets.init();
  emails.init();

  blocks.init();

  editPage.init();

  matchHeight.init();
});
