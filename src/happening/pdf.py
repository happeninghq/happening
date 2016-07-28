"""PDF Tools."""
from wkhtmltopdf.utils import render_pdf_from_template
from wkhtmltopdf.views import PDFResponse
from django.template import loader
from django.template import RequestContext


def render_pdf(request, template_name, context):
    """Return a PDF as a response to a request."""
    return PDFResponse(
        render_pdf_from_template(
            loader.get_template(template_name),
            None, None, context=RequestContext(request, context)))
