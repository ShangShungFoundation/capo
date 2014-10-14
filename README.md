Capo
====

Flexible simple job/task queue engine built on the top of Django framework.
Allows designing and launching complex fully automated jobs straight from admin panel.
Capo can be easily extended with new tasks performing different actions allowing unlimited flexibility.
All jobs are logged together with it results, errors etc. 
Tested with Django 1.6.6 and 1.7 on ubuntu.

Concepts
--------

- *Task* - defines action/s, its parameters and failback behaviour in the case of error.

- *Recipe* - defines sequence of tasks their initial parameters and max quantity of alowed parallel jobs.

- *Job* - defines job parameters for *Recipe* execution, failback bahaviour and stores status of execution. *Job* parameters overwrite *Recipe* parameters. Each job can have various tasks

- *Worker* - defines worker which can be specialized in some recepies


Installation
------------


1. Install::
    
        pip install -e git+https://github.com/ShangShungInstitute/capo#egg=capo

2. Add "capo" to your INSTALLED_APPS in "settings.py"


Extending
---------

Power of capo derives from easy extensibility. You can add more actions (verbs) inheriting from base action located on "capo/actions/action.py:

1. Declare dictionary of 'required_param' together with their type as str, list, int etc. Value of parameter may consist of many types like [str, lits]. "optional_params" and "expected_output" may be declared too.
2. Write documetation for the action in doc string under your action class.
3. Overwrite action's 'run' method.
4. If action returns contributes result wchich later tasks may require result should be apanded to 'self.out["job_param"]' dictionary.


    from capo.actions.actions import Action
    
    class my_action(Action):
        """
        
        {"src": str, "dst": str,}
        """
        expected_param = {"src": str, "dst": str,}
    
        def run(self, action_param):
            ...  
            # action logic goes here
            ...
            # you may return result to job parameters
            self.out["job_param"]["__yuor_result__"] = x
                
If yor action invokes shell command you can inherit from 'cmd' class in '"capo/actions/cmd.py'

To permit capo recognising your action add it to CAPO_ACTIONS dictionary project settings settings.py::

        CAPO_ACTIONS = dict(
            action_name="path.to.your.modlule",
        )

Thanx
-----
to Jakub Ryška https://github.com/coubeatczech for colaboration on the project


