#### 临时服务器

``` 
python -m SimpleHTTPServer 8888
python3 -m http.server 8888
```

### 生成虚拟环境

```
conda create --name test python=3.5 anaconda
python -m ipykernel install --user --name test
```

