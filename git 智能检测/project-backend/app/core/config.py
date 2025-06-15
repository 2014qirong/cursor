import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env'))

class Settings:
    # MySQL配置
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "Admin123")
    DB_NAME: str = os.getenv("DB_NAME", "ai_detect")
    
    # InfluxDB配置
    INFLUXDB_URL: str = os.getenv("INFLUXDB_URL", "http://localhost:8086")
    INFLUXDB_TOKEN: str = os.getenv("INFLUXDB_TOKEN", "A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw==")
    INFLUXDB_ORG: str = os.getenv("INFLUXDB_ORG", "my-org")
    INFLUXDB_BUCKET: str = os.getenv("INFLUXDB_BUCKET", "risk_assessment")

    @property
    def sqlalchemy_url(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

settings = Settings()