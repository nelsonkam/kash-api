import logging

from logtail import LogtailHandler


class CustomLogtailHandler(LogtailHandler):
    def __init__(self):
        super().__init__("ySq7WvubA54nuMoXAxkkiE1A", level=logging.DEBUG)