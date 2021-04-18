class Report:
    def __init__(self, title):
        self.title = title
        self.results = {}

    def add_report(self, target, cpu_usage, memory_usage):
        self.results[target] = {"cpu_usage": cpu_usage, "memory_usage": memory_usage}

    def print_pic(self, save_dir):
        pass
