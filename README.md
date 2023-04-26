# COMP4135 Group Project

## Load Data
### If you want to use you own data
Please edit two Excel file the the code, dan then type;
```
python load_data.py
```
### If you want to use the data from our team
The data is save in data1.pkl and data2.pkl.

## Build Enviroment
```
conda create --name rs python=3.6
virtualenv flask
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
pip install flask
pip install scikit-learn
pip install pyautogui
pip install xlrd
```

## Start
```
python load_data.py
python app.py
```

## Web Content: Copy the URL below and paste it into your browser to open
```
http://127.0.0.1:5000/
```

