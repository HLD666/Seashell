import time


class TaskTest(object):

    def __init__(self, template_id, paras_db, res_db):
        self.temp = template_id
        self.paras_db = paras_db
        self.res_db = res_db

    def start(self):
        print(f"start task with id: {self.temp}")
        time.sleep(300)
        print(f"Finished task, save the result in {self.res_db}")
