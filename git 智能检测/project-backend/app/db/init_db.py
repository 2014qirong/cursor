from app.db.session import engine
from app.models import changes, user, review, notify

# 自动建表
if __name__ == "__main__":
    changes.Base.metadata.create_all(bind=engine)
    user.Base.metadata.create_all(bind=engine)
    review.Base.metadata.create_all(bind=engine)
    notify.Base.metadata.create_all(bind=engine)
    print("数据库表结构已初始化") 