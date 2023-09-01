# Djago 员工管理系统案例
---
│  manage.py      startapp/ migrate<br>
├─app01<br>
│  │  admin.py<br>
│  │  apps.py<br>
│  │  models.py        【orm class】 <br>
│  │  tests.py<br>
│  │  views.py        【return HTML】<br>
│  │  __init__.py<br>
│  ├─migrations<br>
│  │  │  0001_initial.py<br>
│  │  │  __init__.py<br>
│  ├─static           【css js ntml】<br>
│  │  ├─css<br>
│  │  ├─img<br>
│  │  │      111.jpg<br>
│  │  ├─js<br>
│  │  │      jquery-3.7.0.min.js<br>
│  │  └─plugins<br>
│  │      └─bootstrap-3.4.1<br>
│  ├─templates<br>
│  │      depart_add.html<br>
│  │      depart_edit.html<br>
│  │      depart_list.html<br>
└─ERMS0831<br>
    │  asgi.py<br>
    │  settings.py      【database/  appsettings】<br>
    │  urls.py          【route】<br>
    │  wsgi.py<br>
    │  __init__.py<br>
---

### Django 创建项目，app，静态文件
### Models 数据建模 orm操作数据库（mysqlclient）
