import _ from 'lodash';

export const init = () => {
  const syncHeights = () => {
    _.each(document.getElementsByClassName('match-height'), (elem) => {
      const match = document.querySelector(elem.dataset.match);
      console.log(match.clientHeight);
      elem.style.height = match.clientHeight + "px";
    });
  };

  syncHeights();
  // For some reason this can run before the height is actually set correctly.
  // So we run it again
  setTimeout(syncHeights, 1000);
  setTimeout(syncHeights, 3000);
  setTimeout(syncHeights, 10000);
};
