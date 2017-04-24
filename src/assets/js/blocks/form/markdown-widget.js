import $ from 'jquery';

import toMarkdown from 'to-markdown';
import Quill from 'quill';
import '../../../../assets/sass/blocks/markdown-widget.scss';
var showdown  = require('showdown');
var converter = new showdown.Converter();

function setupMarkdownEditor(elem) {
  const $elem = $(elem);
  
  const newElem = $('<div>' + converter.makeHtml(elem.dataset['text']) + '</div>');
  newElem.insertBefore($elem);

  const inputElem = $('<input type="hidden" name="' + $elem.attr('name') + '">')
  inputElem.insertBefore($elem);

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

  const updateInput = () => {
    inputElem.val(toMarkdown(editor.root.innerHTML).replace(/<(?:.|\n)*?>/gm, ''));
  }

  editor.on('text-change', updateInput);

  updateInput();
}

export const init = () => {
  $('.markdown-widget').each(function initMarkdownEditor() {
    setupMarkdownEditor(this);
  });
};
