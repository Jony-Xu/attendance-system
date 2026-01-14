# 考勤管理系统

一个基于 FastAPI + Vue 3 + MySQL 的现代化考勤管理系统。

## 功能特性

### 员工功能
- ✅ Web 端签到/签退
- ✅ 查看当前考勤状态
- ✅ 查看今日考勤记录
- ✅ 添加考勤备注

### 主管功能
- ✅ 设置和管理工作时间
- ✅ 查看员工月度考勤记录
- ✅ 考勤统计分析
- ✅ 员工管理

## 技术栈

### 后端
- **FastAPI** - 现代化的 Python Web 框架
- **SQLAlchemy** - ORM 框架
- **MySQL** - 关系型数据库
- **Pytest** - 测试框架
- **Pydantic** - 数据验证

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Semantic UI** - UI 组件库
- **Axios** - HTTP 客户端
- **Vue Router** - 路由管理
- **Vite** - 构建工具

## 项目结构

```
attendance-system/
├── backend/                 # 后端代码
│   ├── main.py             # 主应用入口
│   ├── config.py           # 配置文件
│   ├── database.py         # 数据库配置
│   ├── models.py           # 数据模型
│   ├── schemas.py          # Pydantic schemas
│   ├── crud.py             # 数据库操作
│   ├── api_employees.py    # 员工 API
│   ├── api_attendance.py   # 考勤 API
│   ├── api_schedules.py    # 工作时间 API
│   ├── conftest.py         # 测试配置
│   ├── test_employees.py   # 员工测试
│   ├── test_attendance.py  # 考勤测试
│   ├── test_schedules.py   # 工作时间测试
│   ├── test_integration.py # 集成测试
│   ├── requirements.txt    # Python 依赖
│   └── .env.example        # 环境变量示例
│
└── frontend/               # 前端代码
    ├── src/
    │   ├── main.js         # 应用入口
    │   ├── App.vue         # 根组件
    │   ├── api.js          # API 封装
    │   └── components/
    │       ├── EmployeeAttendance.vue  # 员工考勤页面
    │       └── AdminDashboard.vue      # 管理后台页面
    ├── index.html
    ├── vite.config.js      # Vite 配置
    └── package.json        # NPM 依赖
```

## 安装和运行

### 前置要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 1. 数据库设置

创建 MySQL 数据库：

```sql
CREATE DATABASE attendance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'attendance_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. 后端设置

```bash
# 进入后端目录
cd attendance-system/backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置数据库连接信息

# 运行数据库迁移（自动创建表）
python main.py  # 启动时会自动创建表

# 或者直接启动服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 http://localhost:8000 启动

API 文档: http://localhost:8000/docs

### 3. 前端设置

```bash
# 进入前端目录
cd attendance-system/frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:3000 启动

### 4. 运行测试

```bash
# 在后端目录下
cd attendance-system/backend

# 运行所有测试
pytest

# 运行特定测试文件
pytest test_employees.py

# 查看测试覆盖率
pytest --cov=. --cov-report=html

# 运行集成测试
pytest test_integration.py -v
```

## 环境变量配置

创建 `backend/.env` 文件：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://attendance_user:your_password@localhost:3306/attendance_db

# 安全配置
SECRET_KEY=your-secret-key-here-change-in-production

# 调试模式
DEBUG=True
```

## API 接口文档

### 员工管理

- `POST /api/employees/` - 创建员工
- `GET /api/employees/` - 获取员工列表
- `GET /api/employees/{id}` - 获取单个员工
- `PUT /api/employees/{id}` - 更新员工信息

### 考勤管理

- `POST /api/attendance/check-in` - 签到
- `POST /api/attendance/check-out` - 签退
- `GET /api/attendance/records` - 获取考勤记录
- `GET /api/attendance/monthly/{year}/{month}` - 获取月度考勤
- `GET /api/attendance/status/{employee_id}` - 获取考勤状态

### 工作时间管理

- `POST /api/schedules/` - 创建工作时间
- `GET /api/schedules/` - 获取工作时间列表
- `GET /api/schedules/active` - 获取当前激活的工作时间
- `PUT /api/schedules/{id}` - 更新工作时间
- `POST /api/schedules/{id}/activate` - 激活工作时间

详细 API 文档请访问: http://localhost:8000/docs

## 使用说明

### 首次使用

1. 启动后端和前端服务
2. 访问 http://localhost:3000
3. 首先进入"管理后台"创建员工和设置工作时间
4. 然后切换到"员工签到"页面进行考勤操作

### 创建测试数据

使用 API 或者 Python 脚本创建测试数据：

```python
import requests

# 创建员工
requests.post('http://localhost:8000/api/employees/', json={
    'employee_id': 'EMP001',
    'name': '张三',
    'email': 'zhangsan@example.com',
    'role': 'employee'
})

# 创建工作时间
requests.post('http://localhost:8000/api/schedules/', json={
    'name': '标准工作时间',
    'check_in_time': '09:00:00',
    'check_out_time': '18:00:00'
})
```

## 测试覆盖

项目包含完整的测试套件：

- ✅ 员工管理测试 (test_employees.py)
- ✅ 考勤功能测试 (test_attendance.py)
- ✅ 工作时间测试 (test_schedules.py)
- ✅ 集成测试 (test_integration.py)

测试覆盖了：
- 所有 API 端点
- 边界条件和错误处理
- 完整的业务流程
- 数据验证

## 生产部署建议

### 后端
1. 使用 Gunicorn 或 uWSGI 作为 WSGI 服务器
2. 配置 Nginx 作为反向代理
3. 使用环境变量管理敏感配置
4. 启用 HTTPS
5. 配置数据库连接池
6. 设置日志记录

### 前端
1. 运行 `npm run build` 构建生产版本
2. 使用 Nginx 或 CDN 托管静态文件
3. 配置正确的 API 地址
4. 启用 Gzip 压缩

### 数据库
1. 定期备份数据库
2. 优化索引和查询
3. 配置主从复制（如需要）

## 常见问题

### 1. 数据库连接失败
- 检查 MySQL 服务是否运行
- 验证 .env 文件中的数据库配置
- 确认数据库用户权限

### 2. 前端无法连接后端
- 确认后端服务已启动
- 检查 vite.config.js 中的代理配置
- 查看浏览器控制台的错误信息

### 3. 测试失败
- 确保所有依赖已安装
- 检查测试数据库配置
- 运行 `pytest -v` 查看详细错误

## 开发路线图

### 第二版计划
- [ ] 用户认证和授权（JWT）
- [ ] 角色权限管理
- [ ] 迟到/早退自动判断
- [ ] 请假管理
- [ ] 加班记录
- [ ] 数据导出（Excel）
- [ ] 邮件通知
- [ ] 移动端适配

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题，请提交 Issue 或联系开发团队。
