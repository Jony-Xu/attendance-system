#!/bin/bash

# 前端启动脚本

echo "🚀 启动考勤管理系统前端..."

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖..."
    npm install
fi

# 启动开发服务器
echo "🎉 启动开发服务器..."
npm run dev
