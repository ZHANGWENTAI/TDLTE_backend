# TDLTE_backend
#### 创建虚拟环境
```
py -3 -m venv venv
```
#### 激活虚拟环境
```
.\venv\Scirpts\activate
```
#### 安装依赖
在项目路径下执行以下命令：
```
pip install -r requirement.txt
```
#### 设置环境变量
```
set FLASK_APP=app.py
set FLASK_ENV=development
```
#### 初始化数据库
```
flask initdb
```
或
```
python -m flask initdb
```
#### 运行
```
flask run
```
或
```
python -m flask run
```
