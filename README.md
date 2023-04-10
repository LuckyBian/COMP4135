# COMP4135 Group Project

## Build Enviroment
```
conda create --name rs python=3.6
virtualenv flask
cd flask
```
## Activate the Enviroment
```
source activate rs
source flask/bin/activate
```
## Install some package
```
pip install Flask
pip install Flask-Table
pip install pandas
pip install numpy
```

## Start
```
python app.py
```

## Web Content: Copy the URL below and paste it into your browser to open
```
http://127.0.0.1:5000/
```

## Problems
```
1. Anime的数据太大，目前使用的是从原始数据中截取了2000条左右。需要找一个合适大小的数据集
2. 推荐系统算法目前使用的是一个最基础的，需要额外添加两个好一点的算法
3. 需要做一个表单对新的用户喜好进行统计，并更新到数据集中
4. 额外： 如果可以找到对应item图片的url，更新到数据集中。图片将会在网页上显示出来。(纯粹为了好看，还没做)
```
