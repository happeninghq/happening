Southampton Code Dojo Website
=========

[![Build Status](https://travis-ci.org/southampton-code-dojo/website.svg?branch=master)](https://travis-ci.org/southampton-code-dojo/website)
[![Coverage Status](https://img.shields.io/coveralls/southampton-code-dojo/website.svg)](https://coveralls.io/r/southampton-code-dojo/website?branch=master)

This is the website for the Southampton Code Dojo. It's currently a work
in progress but will eventually support management of the 
Facebook/Twitter/Meetup accounts, ticketing, membership, and sponsorship.

Pull requests are welcomed.

Requirements
-------
The following must be available and configured:
* python
* virtualenv

Development Requirements
--------
* jshint (Available via: npm install -g jshint)

Getting started
--------
Clone the repository to your disk, and then run setup - this will download 
all requirements and set up the database with some sample events.

Coding Conventions
-------
For Python, follow [PEP8](http://www.python.org/dev/peps/pep-0008/) and
[PEP257](http://www.python.org/dev/peps/pep-0257/). Check that the code
passes using check-standards

check-standards also looks for common mistakes such as unused or double
imports - so try to fix these issues as they are noticed. If any method has a
higher cyclomatic complexity than 10 check-standards will flag it and it
should be changed (split up into multiple methods).

Requirements files should be separated into logical groups, with each
individual requirement commented. All requirements should specify a version.

All functionality implemented should have tests, and all code should follow the
coding conventions mentioned above.

Code coverage should not fall below 90%.