var moment = require('moment');

export const init = () => {
  const form = document.getElementById("email-form")
  if (form != null) {
    const button = form.querySelector("button.submit");
    const input = form.querySelector("[name='sending_range']");
    const reset_state = () => {
      // If "Send once" is selected - the text should be Send Now
      if (input.value == "") {
        button.innerHTML = "Send Now";
      } else {
        const startTime = moment(input.value.split("---")[0]);
        if (startTime.isBefore(moment())) {
          // If the start date is in the past - Send & Schedule
          button.innerHTML = "Send Now & Schedule";
        } else {
          // Otherwise Schedule
          button.innerHTML = "Schedule";
        }
      }
    };
    
    form.querySelector(".datetimerange-widget").addEventListener("change", reset_state);
    reset_state();
  }
};
