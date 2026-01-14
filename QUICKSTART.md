# 快速开始指南

## 5分钟快速上手

### 1. 准备工作

确保已安装以下软件：
- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 2. 数据库设置

```bash
# 登录 MySQL
mysql -u root -p

# 执行以下 SQL
CREATE DATABASE attendance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'attendance_user'@'localhost' IDENTIFIED BY 'Attendance123!';
GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. 后端启动

```bash
# 进入后端目录
cd attendance-system/backend

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，确保数据库配置正确：
# DATABASE_URL=mysql+pymysql://attendance_user:Attendance123!@localhost:3306/attendance_db

# 启动服务器
uvicorn main:app --reload
```

后端启动后访问: http://localhost:8000/docs 查看 API 文档

### 4. 前端启动

打开新的终端窗口：

```bash
# 进入前端目录
cd attendance-system/frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端启动后访问: http://localhost:3000

### 5. 初始化测试数据（可选）

```bash
# 在后端目录下
python init_data.py
```

这将创建：
- 1个主管账号：王经理 (SUP001)
- 3个员工账号：张三 (EMP001)、李四 (EMP002)、王五 (EMP003)
- 3个工作时间方案

### 6. 开始使用

1. 访问 http://localhost:3000
2. 点击"管理后台"查看和管理工作时间
3. 点击"员工签到"进行考勤操作

## 常用命令

### 后端

```bash
# 运行测试
pytest

# 查看测试覆盖率
pytest --cov=. --cov-report=html

# 启动服务器
uvicorn main:app --reload --port 8000
```

### 前端

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 测试账号

运行 `init_data.py` 后可用的测试账号：

| 类型 | 员工编号 | 姓名 | 邮箱 |
|------|---------|------|------|
| 主管 | SUP001 | 王经理 | wang@example.com |
| 员工 | EMP001 | 张三 | zhangsan@example.com |
| 员工 | EMP002 | 李四 | lisi@example.com |
| 员工 | EMP003 | 王五 | wangwu@example.com |

## 功能演示流程

### 场景1：员工签到签退

1. 进入"员工签到"页面
2. 选择员工"张三"
3. 查看当前状态（未签到）
4. 点击"签到"按钮
5. 查看状态变为"已签到"
6. 点击"签退"按钮
7. 查看今日记录

### 场景2：主管管理

1. 进入"管理后台"页面
2. 创建新的工作时间：
   - 名称：弹性工作时间
   - 上班：08:30
   - 下班：17:30
3. 激活新创建的工作时间
4. 查看月度考勤记录：
   - 选择当前年月
   - 查看所有员工的考勤统计

## 故障排除

### 问题1：后端无法连接数据库

**解决方案：**
1. 检查 MySQL 服务是否运行：`mysql.server status`
2. 验证数据库用户和密码
3. 确认 .env 文件配置正确

### 问题2：前端无法连接后端

**解决方案：**
1. 确认后端服务正在运行（http://localhost:8000）
2. 检查浏览器控制台的网络请求
3. 验证 vite.config.js 中的代理配置

### 问题3：导入错误

**解决方案：**
```bash
# 确保在虚拟环境中
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

## 下一步

- 阅读 [完整文档](README.md)
- 查看 [API 文档](http://localhost:8000/docs)
- 运行测试了解更多功能

## 获取帮助

如遇到问题：
1. 查看日志输出
2. 检查 API 文档
3. 运行测试验证功能
4. 提交 Issue

祝使用愉快！🎉
