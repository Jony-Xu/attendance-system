from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
import api_employees
import api_attendance
import api_schedules

app = FastAPI(
    title="考勤管理系统 API",
    description="一个基于 FastAPI 的考勤管理系统",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_employees.router)
app.include_router(api_attendance.router)
app.include_router(api_schedules.router)


@app.on_event("startup")
def on_startup():
    """应用启动时初始化数据库"""
    init_db()


@app.get("/")
def read_root():
    """根路径"""
    return {
        "message": "欢迎使用考勤管理系统 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
