import logging
import sys

_FORMAT = '%(asctime)s%(process)d%(threadName)s' \
          '%(levelname)s%(name)s%(message)s'

_DATE_FORMAT = '%Y-%m-%d %H:%M:%S %z'


log = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
# formatter = jsonlogger.JsonFormatter(_FORMAT, datefmt=_DATE_FORMAT)
# handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)
