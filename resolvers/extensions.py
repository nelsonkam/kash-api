import time

from ariadne.types import ExtensionSync as Extension

from app import db


class QueryExecutionExtension(Extension):
    def __init__(self):
        self.start_timestamp = None
        self.end_timestamp = None
        self.count = 0

    def request_started(self, context):
        self.start_timestamp = time.perf_counter_ns()
        self.count = 0
        event.listen(db.engine, "before_cursor_execute", self.query_callback)

    def request_finished(self, context):
        self.end_timestamp = time.perf_counter_ns()

    def query_callback(self, *_):
        self.count += 1

    def format(self, context):
        return {
            "queries": self.count
        }
