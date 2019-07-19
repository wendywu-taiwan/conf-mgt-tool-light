from RulesetComparer.date_model.json_builder.baseBuilder import BaseBuilder


class JobFailureContentBuilder(BaseBuilder):

    def __init__(self, task_name, exception, trace_back):
        self.task_name = task_name
        self.exception = exception
        self.trace_back = trace_back
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict["task_name"] = self.task_name
        self.result_dict["exception"] = self.exception
        self.result_dict["trace_back"] = self.trace_back

    def get_data(self):
        return self.result_dict
