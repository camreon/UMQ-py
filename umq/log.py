import logging
import sys

log = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)
log.setLevel(logging.INFO)
