from app.tasks.celery_app import celery_app
from app.services.ai import ai_analyzer

@celery_app.task
def async_ai_analyze(diff: str):
    """
    异步AI风险分析任务
    :param diff: 代码变更diff文本
    :return: 分析结果dict
    """
    return ai_analyzer.analyze(diff) 