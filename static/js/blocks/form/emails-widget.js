$(function() {
    $('.emails-widget').each(function() {
        var $this = $(this)
        function email(to, subject, content, start_sending, stop_sending) {
            var r = {
                to: ko.observable(to),
                subject: ko.observable(subject),
                content: ko.observable(content),
                start_sending: ko.observable(start_sending),
                stop_sending: ko.observable(stop_sending),

                deleteEmail: function() {
                  viewModel.emails.remove(this);
                },

                viewPreview: function() {
                    viewModel.activeEmail(this);
                    viewModel.mode("PREVIEW");
                    viewModel.refreshPreview();
                },

                editEmail: function() {
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
                    viewModel.mode("EDITING");
                }
            }

            r.formatted_start_sending = ko.computed(function(){
                if (r.start_sending()) {
                    return r.start_sending().number + ' ' + r.start_sending().type + ' ' + r.start_sending().start;
                }
              return '';
            });

            r.formatted_stop_sending = ko.computed(function() {
                if (r.stop_sending()) {
                  return r.stop_sending().number + ' ' + r.stop_sending().type + ' ' + r.stop_sending().start;
                }
                return '';
            });

            return r;
        }

        var viewModel = {
            emails: ko.observableArray(),
            activeEmail: ko.observable(),
            mode: ko.observable("NONE"), // NONE/EDITING/ADDING

            previewEvent: ko.observable(),
            previewSubject: ko.observable("LOADING"),
            previewContent: ko.observable("LOADING"),

            addEmail: function() {
                viewModel.mode("ADDING");
                $('#add-email-to').val("");
                $('#add-email-subject').val("");
                $('#add-email-content').val("");
                $('#add-email-start-sending-number').val("");
                $('#add-email-stop-sending-number').val("");
            },

            cancelAdding: function() {
                viewModel.mode("NONE");
            },

            confirmAdding: function() {
                var e;
                if (this.mode() == "EDITING") {
                    e = this.activeEmail();
                } else {
                    e = email();
                    viewModel.emails.push(e);
                }
                e.to($('#add-email-to').val());
                e.subject($('#add-email-subject').val());
                e.content($('#add-email-content').val());

                var start_sending = {
                    number: $('#add-email-start-sending-number').val(),
                    type: $('#add-email-start-sending-type').val(),
                    start: $('#add-email-start-sending-start').val()
                };

                var stop_sending = {
                    number: $('#add-email-stop-sending-number').val(),
                    type: $('#add-email-stop-sending-type').val(),
                    start: $('#add-email-stop-sending-start').val()
                };

                e.start_sending(start_sending);
                e.stop_sending(stop_sending);

                viewModel.mode("NONE");
            },

            refreshPreview: function() {
                var data = {
                    subject: viewModel.activeEmail().subject(),
                    content: viewModel.activeEmail().content(),
                    event: viewModel.previewEvent()
                };

                $.getJSON("/staff/emails/preview", data, function(response) {
                    viewModel.previewSubject(response.subject)
                    viewModel.previewContent(response.content)
                });
            }
        }

        viewModel.value = ko.computed(function() {
          // Convert viewModel.emails into json
          return JSON.stringify(ko.toJS(viewModel).emails);
        });

        $this.data('reload', function() {
            viewModel.emails.removeAll();
            value = $this.find('[type="hidden"]').val();
            if (value) {
                value = JSON.parse(value)
                for (i in value) {
                    viewModel.emails.push(email(i.to, i.subject, i.content, i.start_sending, i.stop_sending))
                }
            }
        });

        $this.data('reload')();

        ko.applyBindings(viewModel, this);
    });
});