# multicarlasevers
 
## 使用简介：

 1. 开启CarlaUE并运行。
 2. 在控制台下运行Mult-carla/client下的客户端程序
 ``` shell
    python3 manual_control_selg.py
 ```
 3. 配置carlaservers.yaml文件，其中需要同步的服务器CarlaUE的ip和端口。（至少一台）
 4. 在控制台下运行Mult-carla下的同步服务器程序
 ```
    python3 synchronization.py
 ```

---

## 如果提示找不到carla包
```
cd ~/carla/PythonAPI/carla/dist/
unzip carla-0.9.13-py3.8-linux-x86_64.egg -d carla-0.9.13-py3.8-linux-x86_64
cd carla-0.9.13-py3.8-linux-x86_64
```
接下来打开你的文档编辑器，建立一个setup.py, 将以下内容复制进去。
```
from distutils.core import setup
setup(name='carla',
      version='0.9.13', 
      py_modules=['carla'],
      )
``` 
然后通过pip安装到你的python3当中，从此可以直接import carla了。
```
pip3 install -e ~/carla/PythonAPI/carla/dist/carla-0.9.13-py3.8-linux-x86_64
```

## 设置服务器日志为DEBUG级别可以运行

```
python3 synchronization.py --debug
```

## 在运行CarlaUE的机子上运行Mult-carla/viewer下的程序可以轮流查看服务器内车辆

```
python3 clientview.py
```

## 使用util/下的文件可以更改地图配置
```
python3 config.py --map Town04
```

## 使用Carla-SUMO/下的文件可以运行Carla-SUMO协同仿真。详细见Carla官方文档
