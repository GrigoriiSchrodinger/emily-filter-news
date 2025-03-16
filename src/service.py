from src.feature.RedisManager import RedisQueue

redis = RedisQueue(queue_name="processing", port=6379, db=0)