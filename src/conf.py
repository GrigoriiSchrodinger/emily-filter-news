import os

from src.feature.RedisManager import RedisQueue

redis = RedisQueue(queue_name="processing", host="localhost", port=6379, db=0)
API_KEY = os.getenv('API_KEY')


def return_promt_was_there_post():
    return """
        Вот тебе список новостей которые были за 24 часа. 
        Список - {news_list}.
        Твоя задача, проанализировать список и сказать были ли такая новость, которую я тебе отправлю, в списке. 
        Ты должна ответить True или False, True если новости не было. без блока кода, только текст.
        вот как должен выглядеть твой ответ: 
        """


def return_promt_rate_post():
    return """
        Ты введешь новостной канал, твоя аудитория это русско-говорящий люди от 18 до 40. 
        Твоя задача оценить пост по параметрам. 
        влияние на русский регион - от 1 до 100 
        интерес - от 1 до 100 
        эмоциональное воздействие - от 1 до 100 
        социальная значимость - от 1 до 100.
        три раза проанализируй пост и выведи средний балл для всех параметров. 
        В ответе тебе нужно вернуть в json формате, без блока кода, только текст, твой ответ должен СТРОГО таким:
        {
        "influence": от 1 до 100 
        "interest": от 1 до 100 
        "emotional_impact": от 1 до 100 
        "social_significance": от 1 до 100 
        }
        """


def evaluate_news_post(influence, interest, emotional_impact, social_significance) -> float:
    # Нормализация оценок
    max_score = 100
    influence = influence / max_score
    interest = interest / max_score
    emotional_impact = emotional_impact / max_score
    social_significance = social_significance / max_score

    # вес_влияние
    weight_influence = 0.30
    # вес_интерес
    weight_interest = 0.20
    # вес_эмоциональное_воздействие
    weight_emotional_impact = 0.25
    # вес_социальная_значимость
    weight_social_significance = 0.20

    # Вычисление общего балла с учетом нормализации
    overall_score = (
            influence * weight_influence +
            interest * weight_interest +
            emotional_impact * weight_emotional_impact +
            social_significance * weight_social_significance
    )

    # Приведение общего балла к шкале от 0 до 100
    overall_score *= max_score

    return float(overall_score)
