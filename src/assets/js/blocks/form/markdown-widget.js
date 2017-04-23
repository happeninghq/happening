import $ from 'jquery';

import toMarkdown from 'to-markdown';
import Quill from 'quill';
import '../../../../assets/sass/blocks/markdown-widget.scss';
var showdown  = require('showdown');
var converter = new showdown.Converter();
    


function setupMarkdownEditor(elem) {
  const $elem = $(elem);

  const val = $elem.val();

  const newElem = $('<div>' + converter.makeHtml(val) + '</div>');

  newElem.insertBefore($elem);

  $elem.hide();

  var editor = new Quill(newElem[0], {
    modules: {
      toolbar: [
        ['bold', 'italic'],
        ['blockquote', 'list', 'link'],
        ['image']
      ]
    },
    theme: 'snow'
  });
  

  editor.on('text-change', function(delta, source) {
    $elem.val(toMarkdown(editor.root.innerHTML).replace(/<(?:.|\n)*?>/gm, ''));
  });
}

export const init = () => {
  $('.markdown-widget').each(function initMarkdownEditor() {
    setupMarkdownEditor(this);
  });
};
