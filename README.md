Django + Vue3 全栈博客系统

一个基于 Django 5 和 Vue 3 的前后端分离博客系统，实现了完整的博客基础功能。

🎯 项目简介

这是一个新手练习写的 Django 5 与 Vue 3 的前后端分离练手项目。项目可正常运行。主要实现了博客的基础功能模块，包括用户认证、内容管理、评论系统等。

✨ 功能特性

后端 (Django 5)

• ✅ 用户认证系统（注册、登录、JWT Token）

• ✅ 用户管理（增删查改）

• ✅ 文章管理（增删查改、分类、标签）

• ✅ 评论系统（发表、删除、回复）

• ✅ RESTful API 设计

• ✅ Django REST Framework

• ✅ 数据库迁移

• ✅ 跨域支持 (CORS)

前端 (Vue 3)

• ✅ 响应式设计

• ✅ 组件化开发

• ✅ 状态管理

• ✅ 路由管理

• ✅ 用户界面

• ✅ 文章展示/编辑

• ✅ 评论功能

📁 项目结构

```
blog_djagno5+vue3/
├── blog_backend/              # Django 后端
│   ├── blog_backend/            # 博客应用
│   ├── users/           # 用户应用
│   ├── comment/        # 评论应用
│   │——articles/         #文章应用
│   │——media/            #图片存放目录
│   ├── manage.py
│   └── requirements.txt
│
├── blog_frontend/            # Vue 3 前端
│   ├── src/
│   │   ├── components/  # 公共组件
│   │   ├── views/       # 页面组件
│   │   ├── router/      # 路由配置
│   │   ├── stores/       # 状态管理
│   │   ├── api/         # API 接口
│   │   └── assets/      # 静态资源
│   │   │—— types/       #数据类型
│   ├── package.json
│   └── vite.config.js
│
└── README.md

```
🚀 快速开始

环境要求

• Python 3.13+

• Node.js 22.+

• MySQL 8.0

后端启动

# 克隆项目
git clone <repository-url>
cd blog_djagno5+vue3/backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windos

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver


前端启动

cd ../frontend

# 安装依赖
npm install

# 开发模式运行
npm run dev

# 构建生产版本
npm run build


🔧 配置说明

后端配置

1. 根据需要修改数据库配置，默认用户与密码都为root
2. 已经设置默认后端基础URL  http://localhost:8000
3. 浏览http://localhost:8000/swagger/  查看API接口

前端配置

1. 在api中已经设置默认后端基础URL  http://localhost:8000


主要 API 端点

• POST /user/register/ - 用户注册

• POST /user/login/ - 用户登录

• GET /user/profile/{id} - 用户个人页面

• GET /articles/ - 文章列表

• POST /articles/ - 创建文章

• GET /articles/{id}/ - 文章详情

• POST /comments/ - 发表评论


访问地址：http://localhost:5173

🔄 数据模型

User
```
username（用户名）
email（邮箱）
password（密码）
first_name（名）
last_name（姓）
is_staff（是否管理员）
is_active（是否激活）
is_superuser（是否超级用户）
last_login（最后登录时间）
date_joined（注册时间）
bio（个人简介）
avatar（头像）
created_at（创建时间）
updated_at（更新时间）
```
Article
```
title（标题）
slug（URL标识）
content（内容）
excerpt（摘要）
author（作者）
created_at（创建时间）
updated_at（更新时间）
is_published（是否发布）
cover_image（封面图）
```
Comment
```
content（评论内容）
author（评论作者）
article（关联文章）
created_at（创建时间）
updated_at（更新时间）
is_active（是否发布）
```
📁 数据库设计
```
-- 简化版数据库关系
users
├── id
├── username
├── email
└── created_at

articles
├── id
├── title
├── content
├── author (FK -> users.id)
└── created_at

comments
├── id
├── content
├── author (FK -> users.id)
├── article (FK -> articles.id)
└── created_at
```

🎨 前端技术栈

• Vue 3 - 渐进式 TypeScript 框架

• Vue Router - 路由管理

• Pinia - 状态管理

• Axios - HTTP 客户端

• Element Plus - UI 组件库

• Vite - 构建工具

⚙️ 后端技术栈

• Django 5 - Web 框架

• Django REST Framework - API 框架

• djangorestframework-simplejwt - JWT 认证

• Django CORS Headers - 跨域支持

• Pillow - 图片处理

📱 界面预览

• 首页：文章列表展示

• 文章详情页：内容展示 + 评论

• 用户中心：个人信息管理

• 登录/注册页

🔍 学习重点

1. 前后端分离架构：理解 RESTful API 设计
2. JWT 认证：无状态用户认证
3. 状态管理：Vue 3 的响应式系统
4. 组件通信：父子组件、兄弟组件通信
5. 数据库设计：ORM 模型与关系设计
6. API 设计：RESTful 规范与实践
