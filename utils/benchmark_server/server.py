import requests
import logging
import time
import re

supported_api = {
    "start": "start",
    "stop": "stop",
    "get_log": "log.txt",
    "clear_log": "log",
    "get_status": "status",
}
min_stress_time = 10


def check_response_ok(res) -> bool:
    if not res.ok:
        logging.error(res.text)
        return False
    return True


class Server:
    def __init__(self, config):
        self.base = "//".join(["http:", ":".join([str(config["host"]), str(config["port"])])])

    def _clean_server(self) -> bool:
        return self.stop() and self.clear_log()

    def _get_api(self, api):
        if api not in supported_api.keys():
            return
        return "/".join([self.base, supported_api[api]])

    def start(self, params) -> bool:
        if not self._clean_server():
            logging.error("cannot clean server, please restart server manually")
            return False

        api = self._get_api("start")

        start_timestamp = time.time()

        res = requests.get(api, params=params)
        if not check_response_ok(res): return False

        logging.info("benchmark starts at timestamp:{}".format(start_timestamp))

        time.sleep(10)
        ok, status = self.get_status()

        if not ok or status == "stopped":
            logging.error("benchmark ends too soon, check configs or restart server")

        return True

    def stop(self) -> bool:
        api = self._get_api("stop")
        res = requests.get(api)
        return True if check_response_ok(res) else False

    def get_log(self) -> (bool, str):
        api = self._get_api("get_log")
        res = requests.get(api)
        return (True, res.text) if check_response_ok(res) else (False, "")

    def clear_log(self) -> bool:
        api = self._get_api("clear_log")
        res = requests.delete(api)
        return True if check_response_ok(res) else False

    def get_status(self) -> (bool, str):
        api = self._get_api("get_status")
        res = requests.get(api)
        print(res.text)
        return (True, res.text) if check_response_ok(res) else (False, res.text)

    def get_report(self) -> (bool, dict[str, str]):
        ok, log_file = self.get_log()
        if not ok: return False, None
        lines = log_file.split("\n")
        total_metrics, total_time = 0, 0
        for i, line in enumerate(lines):
            if line.startswith("Summary") and i < len(lines) - 1:
                # get the latest report
                total_metrics = re.findall(r'\d+.\d+|\d+', lines[i+1])[0]
                total_time = re.findall(r'\d+.\d+|\d+', lines[i+1])[1]
        return True, {"total_metrics": total_metrics, "total_time": total_time}

    # def wait_for_stop(self) -> bool:
    #     while (True):
    #         time.sleep(10)
    #         ok, status = self.get_status()
    #         if not ok: return False
    #
    #         if status == "stopped":
    #             break
