import logging
from trollflow import utils

logger = logging.getLogger(__name__)


class WorkflowRunner(object):

    def __init__(self, workflow):
        self.components = [component.keys()[0] for component in workflow["Workflow"]]
        self.workflow = dict((component.items()[0] for component in workflow["Workflow"]))

    def get_class(self, clazz_path):
        return utils.get_class(clazz_path)

    def run(self, context):
        for module in self.components:
            clazz = self.get_class(module)
            component_clazz = clazz()
            component_clazz.slots = sorted(self.workflow[module].keys())

            try:
                component_clazz.pre_invoke()
            except Exception, err:
                msg = "Error in execution of {0}.pre_invoke()".format(
                    component_clazz)
                logger.error(msg)
                raise WorkflowException(msg, err)

            try:
                component_clazz.invoke(context)
            except Exception, err:
                msg = "Error in execution of {0}.invoke()".format(
                    component_clazz)
                logger.error(msg)
                raise WorkflowException(msg, err)
            try:
                component_clazz.post_invoke()
            except Exception, err:
                msg = "Error in execution of {0}.post_invoke()".format(
                    component_clazz)
                logger.error(msg)
                raise WorkflowException(msg, err)


class WorkflowException(Exception):
    pass
    # def __init__(self, msg, error):
    #     self.msg = msg
    #     self.error = error

    # def __str__(self):
    #     return repr("WorkflowException: {0} \nOriginal error: {1]".format(
    #         self.msg,
    #         self.error))
