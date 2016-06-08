import React from 'react';
import Cookies from 'js-cookie';

export const DjangoCSRFToken = React.createClass({

  render: function() {

    const csrftoken = Cookies.get('csrftoken');

    return React.DOM.input(
      {type:"hidden", name:"csrfmiddlewaretoken", value:csrftoken}
      );
  }
});
