DATE_FORMAT = '%d/%m/%y'
TIME_FORMAT = '%H:%M'
DATETIME_FORMAT = DATE_FORMAT + ' ' + TIME_FORMAT

AUTH_ALGO = 'HS256'
AUTH_SCHEME = "bearer"
USER_CLAIM = "sub"

REQUEST_TIMEOUT = 30

MAX_BODY_LOG = 1024 * 1024

MAX_JOB_RETRY = 5