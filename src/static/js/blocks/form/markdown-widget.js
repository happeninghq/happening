/* global EpicEditor:false */
import $ from 'jquery';

/** Epic Editor doesn't support importing - so for now we will include it in the
    page */

function setupMarkdownEditor(elem) {
  const $elem = $(elem);
  const newElem = $('<div></div>');

  newElem.insertBefore($elem);

  $elem.hide();

  const editor = new EpicEditor({
    container: newElem[0],
    clientSideStorage: false,
    textarea: elem[0],
    basePath: '/static/epiceditor/epiceditor',
    theme: {
      base: '../../../lib/epiceditor/themes/base/epiceditor.css',
      editor: '../../../lib/epiceditor/themes/editor/epic-light.css',
      preview: '../../../lib/epiceditor/themes/preview/github.css',
    },
  });
  editor.load();
}

export const init = () => {
  // $('.markdown-widget').each(function initMarkdownEditor() {
  //   setupMarkdownEditor(this);
  // });
};
