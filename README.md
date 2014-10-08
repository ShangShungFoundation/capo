capo
====

Flexible simple job/task queue engine built on the top of django
Tested with Django 1.6.6
Allows designing and launching complex jobs straight from admin panel.
All jobs are loged together with it results, errors etc

Concepts
--------

*Recipe* - defines tasks and initial parameters for a job and max quantity of parallel jobs

*Job* - defines job parameters for Recipe execution, failback bahaviour and stores status of execution. Job parameters overwrite Recipe parameters. Each job can have various tasks

*Task* - defines action, its parameters and failback behaviour in case of error.

*Worker* - defines worker which can be specialized in some recepies


Installation
------------


1. Install::
    
        pip install -e git+https://github.com/ShangShungInstitute/capo#egg=capo

2. Add "capo" to your INSTALLED_APPS in "settings.py"


Thanx
-----
to Jakub Ryška https://github.com/coubeatczech for colaboration on the project


