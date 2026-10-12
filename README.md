# 易民办 · 民生办事向导

> 一款帮助普通用户「看懂办事要求、少跑冤枉路」的民生办事向导 App。

**易民办** 专注于一站式查询民生事项、材料清单、预约导航及避坑要点，让办事群众在去窗口之前就把该准备的材料、该注意的细节弄明白。

> ⚠️ **重要声明**：本工具仅提供办事指引与信息查询，**不替代政务系统、不直接办理任何业务**。所有材料要求、收费标准、办理时限等信息仅供参考，最终以官方窗口要求为准。

---

## ✨ 核心功能

| 功能 | 说明 |
| --- | --- |
| 📚 **办事事项库** | 按「户籍、社保医保、公积金、不动产、婚姻生育、入学、养老补贴、证件办理」八大分类，选择事项与所在区县后生成本地化精简材料清单 |
| 📋 **材料清单** | 区分必备/可选材料、原件/复印件/电子版要求，标注免费/收费、办理时限、线上/线下办理方式 |
| ⚠️ **避坑提示** | 高频驳回原因、照片规格等常见误区提醒，附官方原文入口溯源核验 |
| 📅 **预约与导航** | 直达官方预约入口，展示窗口地址、办公时间、电话、停车/公交提示、取号排队参考 |
| ⏰ **证件与事项提醒** | 手动添加证件或事项，到期前提醒；本地存储为主，不自动抓取证件信息，隐私优先 |
| 📝 **材料模板工具箱** | 个人申请书、情况说明、承诺书等常用模板，支持导出 PDF |
| 📊 **进度聚合中心** | 多个办事事项统一卡片展示，点击跳转对应官方平台（不对接政务 API） |
| 👵 **适老简易模式** | 大字、高对比度、简化菜单、语音朗读，仅保留高频事项与电话联系 |
| 💬 **用户反馈纠错** | 提交信息过时/材料变更/窗口不一致反馈，后台人工审核自迭代 |

---

## 🏗️ 技术架构

- **前端**：UniApp + Vue3 + Pinia（支持 H5、微信小程序多端）
- **后端**：Python FastAPI
- **数据库**：MySQL
- **配色**：浅色系，主色 `#4F7CFF`，界面清晰明了

```
易民办/
├── backend/                # FastAPI 后端
│   ├── app/
│   │   ├── api/            # 路由（meta / matters / tools）
│   │   ├── core/           # 配置、数据库
│   │   ├── models/         # SQLAlchemy ORM 模型
│   │   ├── schemas/        # Pydantic 模型
│   │   └── main.py         # 应用入口
│   ├── scripts/init_db.py  # 建表 + 种子数据
│   ├── requirements.txt
│   └── .env.example
└── frontend/               # UniApp 前端
    ├── src/
    │   ├── pages/          # 各功能页面
    │   ├── utils/          # api / storage / store / helper
    │   ├── pages.json      # 页面与 tabBar 配置
    │   ├── App.vue         # 全局样式
    │   └── main.js
    ├── package.json
    └── vite.config.js
```

---

## 🚀 快速开始

### 1. 后端（FastAPI + MySQL）

```bash
cd backend

# 创建虚拟环境并安装依赖
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 配置数据库
cp .env.example .env
# 编辑 .env，填入 MySQL 连接信息

# 初始化数据库（建表 + 种子数据）
python scripts/init_db.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

接口文档自动生成于：`http://127.0.0.1:8000/docs`

### 2. 前端（UniApp + Vue3）

```bash
cd frontend

npm install

# H5 开发预览
npm run dev:h5

# 微信小程序
npm run dev:mp-weixin

# 构建
npm run build:h5
npm run build:mp-weixin
```

前端默认请求 `http://127.0.0.1:8000/api/v1`，生产环境请在 `src/utils/api.js` 中修改 `BASE_URL`。

---

## 📡 核心 API 一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/v1/meta/categories` | 办事分类列表 |
| GET | `/api/v1/meta/districts` | 区县列表 |
| GET | `/api/v1/matters` | 事项列表（分类/区县/关键词/高频筛选） |
| GET | `/api/v1/matters/{id}` | 事项详情（含材料、避坑、窗口） |
| GET | `/api/v1/templates` | 材料模板列表 |
| POST | `/api/v1/feedbacks` | 提交反馈纠错 |
| GET/POST | `/api/v1/reminders` | 提醒（可选服务端同步） |
| GET/POST | `/api/v1/progress` | 进度聚合（可选服务端同步） |

---

## 🔒 隐私与合规

- 提醒、进度等用户数据**默认本地存储**，不自动抓取证件信息；
- 进度聚合**不对接政务 API**，仅做跳转聚合，降低对接难度与合规风险；
- 事项库信息由后台人工维护，用户反馈经审核后更新，形成自迭代机制。

---

## 📄 免责声明

本项目为学习与工具性质的开源项目，所展示的办事事项、材料要求、收费标准、办理时限等信息为示范数据，**不构成任何办事依据**。实际办理请以当地政务部门官方发布为准。

---

## 📝 License

MIT
