# ExHW   
瀚文75扩展模块水墨屏图片刷写工具

### INSTALL

- 安装python【[python3.9](https://www.python.org/ftp/python/3.9.10/python-3.9.10-amd64.exe)】

- 安装第三方依赖

  ```shell
  pip install -r requirements.txt
  ```

* 注册和风天气账号，创建项目，申请[KEY](https://dev.qweather.com/docs/configuration/project-and-key/)，免费的就行

* 重命名`conf.yaml.sample`为`conf.yaml`，并修改key和location。
  `location`可通过[城市搜索服务](https://dev.qweather.com/docs/api/geoapi/city-lookup/)获取或直接在和风天气提供的[China-City-List](https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv)中查找

  ```yaml
  defaults:
    key: "1112816xx"
    location: "xxxa7ca05c5axxxe84b03effae0adxxx"
  ```

* 执行 `app.py`

  ```shell
  python3 app.py
  ```

  




### PREVIEW
![图片预览](docs/output.png#pic_center)

### ♥️ ACKNOWLEDGEMENT

- [UpdateWeather](https://github.com/HellSakura/UpdateWeather)