Southampton Code Dojo Website
=========

This is the website for the Southampton Code Dojo. It's currently a work
in progress but will eventually support management of the 
Facebook/Twitter/Meetup accounts, ticketing, membership, and sponsorship.

Requirements
-------
The following must be available and configured:
* python
* virtualenv

Development Requirements
--------
* flake8 (Available via: pip install flake8)
* pep258 (Available via: pip install pep258)
* jshint (Available via: npm install -g jshint)

Coding Conventions
-------
For Python, follow [PEP8](http://www.python.org/dev/peps/pep-0008/) and
[PEP257](http://www.python.org/dev/peps/pep-0257/). Check that the code
passes using check-standards.sh.

check-standards also looks for common mistakes such as unused or double
imports - so try to fix these issues as they are noticed. If any method has a
higher cyclomatic complexity than 10 check-standards will flag it and it
should be changed (split up into multiple methods).

Requirements files should be separated into logical groups, with each
individual requirement commented. All requirements should specify a version.


Development is managed on [Pivotal Tracker](https://www.pivotaltracker.com/n/projects/1215654).
When working on a feature from the backlog, that feature should not be marked
as complete until it is has fully implemented the requirements from the
backlog item, has tests to prove it, and all of this code follows the coding
conventions mentioned above.