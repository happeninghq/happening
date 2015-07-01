Standards
================

For Python, follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ and `PEP257 <https://www.python.org/dev/peps/pep-0257/>`_. With SCSS we follow a loose form of `CSSGuidelin.es <http://cssguidelin.es/>`_ and OOCSS with BEM naming convention. Existing styles can be viewed in styleguide.html.

Check that the code passes using ``check-standards``.

``check-standards`` also looks for common mistakes such as unused or double imports - these issues should be fixed before they are committed. If any method has a higher cyclomatic complexity than 10 check-standards will flag it and it should be changed (split up into multiple methods).

Requirements files should be separated into logical groups, with each individual requirement commented. All requirements should specify a version.

All functionality implemented should have tests, and all code should follow the coding conventions mentioned above.

Code coverage should not fall below 90%.