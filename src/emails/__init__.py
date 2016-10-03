"""Email management."""
from django.template import Context, Template


def render_email(text, user, event=None):
    """Render an email for the given user and event.

    This can be called separately for the subject and content.

    It will include markdown which can then be rendered for use in
    HTML emails.
    """
    # We have to run the django template renderer first
    # this will allow us to send a html and non-html version
    # of the email

    var = {"user": user}
    if event:
        var["event"] = event
    context = Context(var)
    return Template(text).render(context)
