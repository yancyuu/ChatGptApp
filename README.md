# CHATGPT_MANAGER



[![](https://img.shields.io/badge/python-3-brightgreen.svg)](https://www.python.org/downloads/)
<img src="https://img.shields.io/badge/license-GPL--3.0-brightgreen">

*仅限学习交流使用，禁止商用。未经授权禁止转载*


##### 本项目遵守GPL-3.0开源协议

##### 您可以使用本项目for yourself，如果您使用本项目获利（包括但不限于商用、程序代做以及其他私活），则不被允许；

##### 如果您未经允许使用本项目获利，本人保留因侵权连带的一切追责行为；同时造成的法律纠纷与本人无关。



### 求求大家给个star吧！！这个对我真的很重要！！

本程序是一个方便管理各个api的后端框架。

目前支持的写入类型如下：
- MongoDB数据库

如果您需要其他数据库支持，联系我们或者您添加后提PR。

***

**一个用于管理第三方api的后端框架，已经接入openai作为尝试。**

**虽然我已经尽量编写详细的使用文档，即便如此：**

**如果您是发现了bug或者有什么更好的提议，欢迎给我发邮件提issues、或PR，但是跟程序运行有关的所有问题请自行解决或查看[这里](https://github.com/yancyuu/spider/issues)。**

**不接受小白提问，自行研究。文档比较完善，阅读完完整文档后如还有有疑问，提问时请展示你思考验证的过程。**

***

## 开发计划

### 已支持
- 微信授权登录。

- 使用jwt生成token，可用作api权限管理。

- openai的编辑，文本对话，获取训练模型等接口。


### 计划支持(最近几个月很忙，可能没办法更新，周末如果有空可能会更新)

- 前端小程序界面

- 以api为维度的后台管理

## 环境配置
语言：python3.7

系统：Windows/Linux/MacOS

运行依赖：mongo4.2,redis

容器环境配置：

查看 requirements.txt 一键配置：

    pip install -r requirements.txt

## 使用方法：


### 配置配置文件
首先在根目录创建.env文件，参数意义如下,将mongo和redis相关修改为自己的配置。
vim .env
     
    # 应用相关配置
    API_VERESION=$VERSION
    VERSION_DIR=$VERSION
    APPNAME='api-service'
    JWT_TOKEN_SECRET = '123456'
    JWT_ISSUER = 'API'
    TOKEN_EXPIRED = 86400
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python'
    
    # 日志相关配置
    LOGGER_CATEGORY=INFO,DEBUG,ERROR
    LOGGER_ENABLE_CONSOLE=true
    LOGGER_ENABLE_SYSLOG=false
    LOGGER_SYSLOG_HOST=logger.server
    LOGGER_SYSLOG_PORT=514
    LOGGER_SYSLOG_FACILITY=local7
    LOGGER_ENABLE_FILE=false
    LOGGER_FILE_DIRECTORY=$HOME/logs/$APPNAME/$VERSION
    
    # MongoDB数据库配置
    MONGODB_ADDRESS=''
    MONGODB_PORT=
    MONGODB_USER_NAME=''
    MONGODB_ROOT_PASSWORD=''
    
    # Redis配置
    REDIS_ADDRESS=''
    REDIS_PORT=
    REDIS_PASSWORD=''
    
    # openai配置
    OPENAI_API_KEY = ""
    OPENAI_ORGANIZATION = ""

    


### 运行程序
这里介绍两种方式

#### 1.直接启动项目

配置好配置文件后，直接根目录启动 
cd /ChatGptApp && python app.py

#### 2.镜像启动

**为了保证安全，最好将环境变量在初始化项目的时候打入镜像。我这使用docker构建初始化镜像，步骤如下**
1. 编写初始化构建文件，将初始化环境变量和依赖项打入镜像：vim init

       FROM python:3.10 AS base
       RUN mkdir /app
       WORKDIR /app
       COPY requirements.txt .
       COPY .env .
       COPY config.py .
       RUN pip install --no-cache-dir --upgrade pip -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

2. 执行初始构建并生成镜像
  
       docker build -f init -t base:v1.0 .
3. 执行部署项目的构建文件（见项目中的Dockerfile）

       docker build -t chatai_service:v1.0 .

4. 运行容器

       docker --name chatai_service -p 5000:5000 /bin/bash 

