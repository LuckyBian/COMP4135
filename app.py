#加载一些包，不要动
from flask import Flask, flash, render_template, request, redirect, session, url_for
import pickle
import pandas as pd 
import ast
import Recommenders as R
app = Flask(__name__)


# 将pkl文件导入
def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

# app 从这里启动，如果不附加文字，跳转到index.html
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', login=True, url_link=default_url, df=data['df'])


# 当附加上 dashboard 时，跳转到dashboard.html,加载需要的数据
@app.route('/dashboard/', methods=['GET','POST'])
def dashboard():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        song_choice = ast.literal_eval(str(request.form.get('song_choice')))  # Convert string dict to actual dict
        if song_choice:
            user_id = int(song_choice['user_id'])
            url_link = song_choice['url_link']

            row = data['df'].loc[data['df']['url_link'] == url_link].iloc[0]    # extract corresponding row
            row['user_id'] = user_id                                            # change to correct user_id
            data['history'].append(row)  

            df_combined = data['df'].append(pd.DataFrame(data['history']), ignore_index=True)   # combine to one df
            models['item'].create(df_combined, 'user_id', 'title')              # update df

        else:   # has to be a different user_id or started from '/'
            data['history'] = []    # reset history
            url_link = default_url  # reset url

    return render_template('dashboard.html', 
                           df=data['df'], 
                           user_id=user_id, 
                           history=data['history'],
                           pop_model=models['pop'], 
                           login=False,
                           url_link=url_link)

if __name__ == "__main__":   
    # Load database
    df = load_data('data.pkl')
    data = {'df':df}
    user_id = None

    # url 不要动，如果可以找到 anime的图片，可以用url导入，现在还没写好
    default_url = 'https://www.baidu.com'
    
    # 在这里加载推荐算法
    pop_model = R.popularity_recommender_py()
    pop_model.create(df, 'user_id', 'title')
    pop_rec = pop_model.recommend(df.iloc[0]['user_id'])

    #给推荐算法起一个名字，放进model里面
    models = {'pop':pop_rec}

    app.run(debug=True)
