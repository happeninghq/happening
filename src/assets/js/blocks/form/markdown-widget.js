import $ from 'jquery';

import toMarkdown from 'to-markdown';
import Quill from 'quill';
import '../../../../assets/sass/blocks/markdown-widget.scss';
import { markdown } from 'markdown';


function setupMarkdownEditor(elem) {
  const $elem = $(elem);

  const newElem = $('<div>' + markdown.toHTML($elem.val()) + '</div>');

  newElem.insertBefore($elem);

  // $elem.hide();

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
