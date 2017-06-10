# LimeOJ

[![Build Status](https://travis-ci.com/Ohllie/LimeOJ.svg?token=2QPxw9oUgaBRLGvyxUjx&branch=master)](https://travis-ci.com/Ohllie/LimeOJ)

LimeOJ is an open source online judge created with Python.<br>
**Use with caution, the judge is not secure at the moment!**

# Development

Vagrant can be used to set up a development environment quickly.

## Setting up the environment

Controller:

- Duplicate the `lime/.env.example` to `lime/.env` and fill in the values
  - For testing purposes set DB_URL to `"mysql://root:@localhost/lime"`
  - `FLASK_SECRET` should be set to a fairly long randomly generated string
  - `LIME_DEBUG=1` can be appended to the file to enable Flask debugging
- `vagrant up`
- `vagrant ssh controller`
- `./deploy test`

Master:
- `vagrant ssh master`
- Build the docker image `cd /lime-code/docker && docker build -t grader_docker .`
- Fetch the tests with `/lime-code/fetch_tests.sh`

## Guidelines

- Use PEP8-ish code, verify with the pep8 tool using `lime/pep8.cfg`
