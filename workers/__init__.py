from huey import RedisHuey, crontab
import config
from utils import bot
huey = RedisHuey(url=config.REDIS_URL)

@huey.periodic_task(crontab(hour="08", minute="00"))
def post_metrics():
    return bot.post_metrics()
