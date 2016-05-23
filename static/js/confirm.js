import $ from 'jquery';
import Cookies from 'js-cookie';

export const init = () => {
  const csrftoken = Cookies.get('csrftoken');
  $('body').on('click', '.confirm', function initConfirm() {
    if (confirm($(this).data('confirm'))) {
      if ($(this).attr('href')) {
        $('<form action=' + $(this).attr('href') +
          ' method="POST"><input type="hidden" name="csrfmiddlewaretoken" value="' +
          csrftoken + '"></form>').submit();
        return false;
      }
      // For forms etc.
      return true;
    }
    return false;
  });
};
