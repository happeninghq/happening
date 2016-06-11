import Cookies from 'js-cookie';
import $ from 'jquery';

export const init = () => {
    const csrftoken = Cookies.get('csrftoken');

    const csrfSafeMethod = (method) => (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))

    $.ajaxSetup({
        beforeSend: function beforeSend(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
};