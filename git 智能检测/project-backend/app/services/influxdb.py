from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class InfluxDBService:
    def __init__(self):
        self.client = InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = settings.INFLUXDB_BUCKET
        self.org_id = "0e99aeecad56cd00"  # 使用实际的组织ID
    
    def write_risk_assessment(self, change_id: str, probability: float, impact: str, 
                            risk_level: str, analysis_result: dict = None):
        """写入风险评估数据到InfluxDB"""
        try:
            point = Point("risk_assessment") \
                .tag("change_id", change_id) \
                .tag("impact", impact) \
                .tag("risk_level", risk_level) \
                .field("probability", probability) \
                .time(datetime.utcnow(), WritePrecision.NS)
            
            # 如果有详细分析结果，添加更多字段
            if analysis_result:
                if "confidence" in analysis_result:
                    point = point.field("confidence", analysis_result["confidence"])
                if "risk_score" in analysis_result:
                    point = point.field("risk_score", analysis_result["risk_score"])
                if "category" in analysis_result:
                    point = point.tag("category", analysis_result["category"])
            
            self.write_api.write(bucket=self.bucket, org=self.org_id, record=point)
            logger.info(f"Successfully wrote risk assessment data for change_id: {change_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write risk assessment data: {str(e)}")
            return False
    
    def write_ai_analysis(self, change_id: str, analysis_type: str, result: dict):
        """写入AI分析结果到InfluxDB"""
        try:
            point = Point("ai_analysis") \
                .tag("change_id", change_id) \
                .tag("analysis_type", analysis_type) \
                .field("result", str(result)) \
                .time(datetime.utcnow(), WritePrecision.NS)
            
            # 如果结果包含数值字段，单独添加
            if isinstance(result, dict):
                for key, value in result.items():
                    if isinstance(value, (int, float)):
                        point = point.field(key, value)
            
            self.write_api.write(bucket=self.bucket, org=self.org_id, record=point)
            logger.info(f"Successfully wrote AI analysis data for change_id: {change_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write AI analysis data: {str(e)}")
            return False
    
    def close(self):
        """关闭InfluxDB连接"""
        if self.client:
            self.client.close()

# 全局InfluxDB服务实例
influxdb_service = InfluxDBService()