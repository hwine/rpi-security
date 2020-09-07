# -*- coding: utf-8 -*-

import sys
import os
import logging


logger = logging.getLogger()


def exit_cleanup():
    if 'camera' in vars():
        camera.stop_recording()
        camera.close()

def exit_clean(signal=None, frame=None):
    logger.info("rpi-security stopping...")
    exit_cleanup()
    sys.exit(0)

def exit_error(message):
    logger.critical(message)
    print("unexpected exception")
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

    raise SystemExit(99)
    print("post raise")
    exit_cleanup()
    sys.exit(1)

def exception_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(repr(value)))
    print("unexpected exception")
    import sys, traceback
    traceback.print_exc(file=sys.stdout)

    raise SystemExit(66)
    print("post raise")
