# URP教务系统辅助工具

## 0x00 关于

本项目是一个URP教务系统辅助工具，包含查分，评教，选课，教师录入分数等功能。
项目包含一个基于Flask的简易web服务，用于对接我自己laravel写的前端，此web服务无任何用户认证功能，全部为get接口。

## 0x01 使用

请先安装 **virtualenv**

安装所需Python库

```pip install -r requirements.txt```

使用前请先修改conf文件夹中的url配置文件

每个模块使用前需以数组传入用户学号及密码

```[num, pwd]```
