import $ from 'jquery';

import toMarkdown from 'to-markdown';
import Quill from 'quill';
import 'quill/dist/quill.base.css';
import 'quill/dist/quill.snow.css';
import '../../../../assets/sass/blocks/markdown-widget.scss';
import { v4 } from 'uuid';
import { markdown } from 'markdown';


function setupMarkdownEditor(elem) {
  const $elem = $(elem);
  const id = v4();

  const toolbar = $(`<div id="i_${id}" class="toolbar">
    <span class="ql-format-group">
    <span title="Bold" class="ql-format-button ql-bold"></span>
    <span class="ql-format-separator"></span>
    <span title="Italic" class="ql-format-button ql-italic"></span>
    </span>
    <span class="ql-format-group">
    <span title="List" class="ql-format-button ql-list"></span>
    <span class="ql-format-separator"></span>
    <span title="Bullet" class="ql-format-button ql-bullet"></span>
    </span>
    </div>`);

  const newElem = $('<div>' + markdown.toHTML($elem.val()) + '</div>');

  newElem.insertBefore($elem);
  toolbar.insertBefore(newElem);

  $elem.hide();

  var editor = new Quill(newElem[0], {
    modules: {
      toolbar: { container: '#i_' + id },
    },
    theme: 'snow'
  });
  

  editor.on('text-change', function(delta, source) {
    $elem.val(toMarkdown(editor.getHTML()).replace(/<(?:.|\n)*?>/gm, ''));
  });
}

export const init = () => {
  $('.markdown-widget').each(function initMarkdownEditor() {
    setupMarkdownEditor(this);
  });
};
