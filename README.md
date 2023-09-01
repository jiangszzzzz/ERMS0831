# Djago 员工管理系统案例
---

│  manage.py      startapp/ migrate
├─app01
│  │  admin.py
│  │  apps.py
│  │  models.py       orm class 
│  │  tests.py
│  │  views.py        return HTML
│  │  __init__.py
│  ├─migrations
│  │  │  0001_initial.py
│  │  │  __init__.py
│  ├─static           css js ntml
│  │  ├─css
│  │  ├─img
│  │  │      111.jpg
│  │  │
│  │  ├─js
│  │  │      jquery-3.7.0.min.js
│  │  │
│  │  └─plugins
│  │      └─bootstrap-3.4.1
│  │
│  ├─templates
│  │      depart_add.html
│  │      depart_edit.html
│  │      depart_list.html
└─ERMS0831
    │  asgi.py
    │  settings.py      database/  appsettings
    │  urls.py          route
    │  wsgi.py
    │  __init__.py

## Django 开发 员工管理系统案例

### Django 创建项目，app，静态文件

### Models 数据建模 orm操作数据库（mysqlclient）
