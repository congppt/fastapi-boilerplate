from constants.env import IS_LOCAL, ENV, SENTRY_DSN

REQUEST_TIMEOUT = 30

class Discord:
    DISCORD_BASE = "https://discord.com/api"
    NOTIFICATION_PATH = "/webhooks/"

class Sentry:
    DSN = SENTRY_DSN
    TRACE_RATE = 1.0
    PROFILE_RATE = 1.0
    DEBUG = IS_LOCAL
    ENVIRONMENT = ENV
