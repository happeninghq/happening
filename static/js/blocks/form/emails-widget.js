import $ from 'jquery';
import ko from 'knockout';

export const init = () => {
  $('.emails-widget').each(function initEmailsWidget() {
    const $this = $(this);

    const viewModel = {
      emails: ko.observableArray(),
      activeEmail: ko.observable(),
      mode: ko.observable('NONE'), // NONE/EDITING/ADDING

      previewEvent: ko.observable(),
      previewSubject: ko.observable('LOADING'),
      previewContent: ko.observable('LOADING'),

      addEmail() {
        viewModel.mode('ADDING');
        $('#add-email-to').val('');
        $('#add-email-subject').val('');
        $('#add-email-content').val('');
        $('#add-email-start-sending-number').val('');
        $('#add-email-stop-sending-number').val('');
      },

      cancelAdding() {
        viewModel.mode('NONE');
      },

      confirmAdding() {
        let e;
        if (this.mode() === 'EDITING') {
          e = this.activeEmail();
        } else {
          e = email();
          viewModel.emails.push(e);
        }
        e.to($('#add-email-to').val());
        e.subject($('#add-email-subject').val());
        e.content($('#add-email-content').val());

        const startSending = {
          number: $('#add-email-start-sending-number').val(),
          type: $('#add-email-start-sending-type').val(),
          start: $('#add-email-start-sending-start').val()
        };

        const stopSending = {
          number: $('#add-email-stop-sending-number').val(),
          type: $('#add-email-stop-sending-type').val(),
          start: $('#add-email-stop-sending-start').val()
        };

        e.start_sending(startSending);
        e.stop_sending(stopSending);

        viewModel.mode('NONE');
      },

      refreshPreview() {
        const data = {
          subject: viewModel.activeEmail().subject(),
          content: viewModel.activeEmail().content(),
          event: viewModel.previewEvent(),
        };

        $.getJSON('/staff/emails/preview', data, (response) => {
          viewModel.previewSubject(response.subject);
          viewModel.previewContent(response.content);
        });
      },
    };


    function email(to, subject, content, startSending, stopSending) {
      const r = {
        to: ko.observable(to),
        subject: ko.observable(subject),
        content: ko.observable(content),
        start_sending: ko.observable(startSending),
        stop_sending: ko.observable(stopSending),

        deleteEmail() {
          viewModel.emails.remove(this);
        },

        viewPreview() {
          viewModel.activeEmail(this);
          viewModel.mode('PREVIEW');
          viewModel.refreshPreview();
        },

        editEmail() {
          viewModel.activeEmail(this);
          $('#add-email-to').val(this.to());
          $('#add-email-subject').val(this.subject());
          $('#add-email-content').val(this.content());
          $('#add-email-start-sending-number').val(this.start_sending().number);
          $('#add-email-start-sending-type').val(this.start_sending().type);
          $('#add-email-start-sending-start').val(this.start_sending().start);
          $('#add-email-stop-sending-number').val(this.stop_sending().number);
          $('#add-email-stop-sending-type').val(this.stop_sending().type);
          $('#add-email-stop-sending-start').val(this.stop_sending().start);
          viewModel.mode('EDITING');
        }
      }

      r.formatted_start_sending = ko.computed(() => {
        if (r.start_sending()) {
          return `${r.start_sending().number} ${r.start_sending().type} ${r.start_sending().start}`;
        }
        return '';
      });

      r.formatted_stop_sending = ko.computed(() => {
        if (r.stop_sending()) {
          return `${r.stop_sending().number} ${r.stop_sending().type} ${r.stop_sending().start}`;
        }
        return '';
      });

      return r;
    }

    viewModel.value = ko.computed(() =>
      // Convert viewModel.emails into json
      JSON.stringify(ko.toJS(viewModel).emails)
    );

    $this.data('reload', () => {
      const value = $this.find('[type="hidden"]').val();
      viewModel.emails.removeAll();
      if (value) {
        const decodedValue = JSON.parse(value);
        for (const i in decodedValue) {
          viewModel.emails.push(
            email(
              decodedValue[i].to,
              decodedValue[i].subject,
              decodedValue[i].content,
              decodedValue[i].start_sending,
              decodedValue[i].stop_sending));
        }
      }
    });

    $this.data('reload')();

    ko.applyBindings(viewModel, this);
  });
};
