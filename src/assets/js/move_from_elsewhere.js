// This allows pulling in an element from another part of the page
import $ from 'jquery';

export const init = () => {
  $('.move-from-elsewhere').each((i, el) => {
    const move = $(el.dataset.move);
    move.insertAfter(el);
    el.remove();
  });
};
