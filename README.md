Capo
====

Flexible simple job/task queue engine built on the top of Django framework.
Allows designing and launching complex fully automated jobs straight from admin panel.
Capo can be easily extended with new tasks performing different actions allowing unlimited flexibility.
All jobs are logged together with it results, errors etc. 
Tested with Django 1.6.6 and 1.7 on ubuntu.

Concepts
--------
*Task* - defines action/s, its parameters and failback behaviour in the case of error.

*Recipe* - defines sequence of tasks their initial parameters and max quantity of alowed parallel jobs.

*Job* - defines job parameters for *Recipe* execution, failback bahaviour and stores status of execution. *Job* parameters overwrite *Recipe* parameters. Each job can have various tasks

*Worker* - defines worker which can be specialized in some recepies


Installation
------------


1. Install::
    
        pip install -e git+https://github.com/ShangShungInstitute/capo#egg=capo

2. Add "capo" to your INSTALLED_APPS in "settings.py"


Thanx
-----
to Jakub Ryška https://github.com/coubeatczech for colaboration on the project


