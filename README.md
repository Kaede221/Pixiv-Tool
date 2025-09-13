# Pixiv Tool

一个基于 Gradio 的 Pixiv 数据获取与管理工具，支持数据爬取、合并、分析与清洗功能。

## ✨ 功能特点

### 核心功能

- **数据获取**：支持两种模式（插画/用户），通过 URL 爬取 Pixiv 数据
- **数据管理**：合并 JSON 数据文件，统一管理本地数据库
- **数据分析**：查看数据库信息、标签占比统计、高频标签排行
- **数据清洗**：按 PID 删除无效或不需要的记录

### 技术栈

- Python 3.x
- Gradio（UI 框架）
- JSON（数据存储）

## 🚀 快速开始

### 环境准备

1. 克隆项目到本地
2. 安装依赖（需 Python 3.8+）：

```bash
pip install gradio requests
```

### 配置文件

在项目根目录创建 `config.json` 格式如下:

```json
{
  "database_name": "pixiv_data.json",  // 数据库文件名
  "user": {
    "cookie": "你的 Pixiv Cookie",       // 从浏览器获取
    "user_agent": "你的 User-Agent"     // 浏览器请求头
  }
}
```

### 启动应用

```bash
python app.py
```

## ⚠️ 注意事项

1. 本工具仅用于个人学习研究，请勿过度爬取数据
2. Cookie 有效期有限，过期后需重新更新 `config.json`
3. 数据库文件位于 `jsons/` 目录下，建议定期备份

## 许可证

本项目采用 MIT 许可证.