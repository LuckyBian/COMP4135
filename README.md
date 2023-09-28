# COMP4135 Group Project
"Welcome to our Anime Recommendation Engine! If you're a fan of Japanese animated series and films, this is the place for you. Our system is tailored to provide you with the most accurate anime recommendations based on your unique preferences. Whether you're into action-packed adventures, heartwarming romance, intricate fantasies, or mind-bending thrillers, our engine dives deep into an extensive database to suggest titles that match your tastes. Using advanced algorithms and user feedback, we ensure that every recommendation is tailored to your liking. Dive in, explore a world of anime, and discover new favorites today!"
## Load Data
### If you want to use you own data
Please edit two Excel file in the code, dan then type;
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
python app.py
```

## Web Content: Copy the URL below and paste it into your browser to open
```
http://127.0.0.1:5000/
```

