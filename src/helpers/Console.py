class Console(object):
    def __init__(self):
        self.templates = {
            "primary" : "%s",
            "info" : "\033[36m%s\033[0m",
            "danger" : "\033[31m%s\033[0m",
            "warning" : "\033[33m%s\033[0m",
            "success" : "\033[32m%s\033[0m"
        }
    def print(self, msg, msgtype="info"):
        '''print the msg'''
        if not self.templates.__contains__(msgtype):
            msgtype = "primary"
        template = self.templates[msgtype]
        print(template %msg)
