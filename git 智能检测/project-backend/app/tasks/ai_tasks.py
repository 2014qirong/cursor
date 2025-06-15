from app.tasks.celery_app import celery_app
from app.services.ai import ai_analyzer
from app.services.influxdb import influxdb_service
import logging
import uuid

logger = logging.getLogger(__name__)

@celery_app.task
def async_ai_analyze(diff: str, change_id: str = None):
    """
    异步AI风险分析任务
    :param diff: 代码变更diff文本
    :param change_id: 变更ID，如果为空则生成一个
    :return: 分析结果dict
    """
    try:
        # 如果没有提供change_id，生成一个
        if not change_id:
            change_id = str(uuid.uuid4())
        
        # 执行AI分析
        analysis_result = ai_analyzer.analyze(diff)
        
        # 写入InfluxDB
        if analysis_result:
            # 提取风险评估数据
            probability = analysis_result.get('probability', 0.0)
            impact = analysis_result.get('impact', 'unknown')
            risk_level = analysis_result.get('risk_level', 'low')
            
            # 写入风险评估数据
            influxdb_service.write_risk_assessment(
                change_id=change_id,
                probability=probability,
                impact=impact,
                risk_level=risk_level,
                analysis_result=analysis_result
            )
            
            # 写入AI分析详细结果
            influxdb_service.write_ai_analysis(
                change_id=change_id,
                analysis_type="risk_assessment",
                result=analysis_result
            )
            
            logger.info(f"AI analysis completed and data written to InfluxDB for change_id: {change_id}")
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error in async_ai_analyze: {str(e)}")
        return {"error": str(e)}