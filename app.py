from flask import Flask, flash, render_template, request, redirect, session, url_for
import pickle
import pandas as pd
import ast
import Recommenders as R
import os
import pyautogui
from flask import jsonify
import os
import sys
import subprocess
app = Flask(__name__)
app.secret_key = os.urandom(24)


# Functions for loading and saving data
def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def save_data(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def combined_recommendations(user_id, pop_model, item_similarity_model, alpha=0.5):
    # Get the popularity-based recommendations
    pop_recs = pop_model

    # Get the item similarity-based recommendations
    item_sim_recs = item_similarity_model.recommend(user_id)
    print("Type of item_sim_recs:", type(item_sim_recs))

    # Combine the two recommendation sets
    pop_recs['score'] = pop_recs['score'] * alpha
    item_sim_recs['score'] = item_sim_recs['score'] * (1 - alpha)

    combined_recs = pd.concat([pop_recs, item_sim_recs])
    combined_recs = combined_recs.groupby('title', as_index=False)['score'].sum()

    # Sort the recommendations by score and reset the index
    combined_recs = combined_recs.sort_values('score', ascending=False).reset_index(drop=True)

    return combined_recs




@app.route('/question2/<int:user_id>', methods=['GET', 'POST'])
def question2(user_id):
    if request.method == 'POST':
        ratings = request.form.to_dict()
        print(ratings)

        # Load the data2.pkl file
        data2_df = pd.read_pickle('data2.pkl')

        # Load the data.pkl file
        data_df = pd.read_pickle('data2.pkl')

        new_rows = []

        for title, rating in ratings.items():
            item_id = data_df.loc[data_df['title'] == title, 'item_id'].iloc[0]
            new_rows.append({'user_id': user_id, 'item_id': item_id, 'title': title, 'rating': int(rating)})

        # Create a new DataFrame from the new_rows list
        new_data = pd.DataFrame(new_rows)

        # Append the new rows to the data2_df DataFrame
        data2_df = pd.concat([data2_df, new_data], ignore_index=True)

        # Save the updated data2_df to data2.pkl
        data2_df.to_pickle('data2.pkl')
        pyautogui.hotkey('command', 's')

        return redirect(url_for('index'))

    checked_comics = session['checked_comics']
    return render_template('question2.html', user_id=user_id, checked_comics=checked_comics)



# Routes and functions
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', login=True, url_link=default_url, df=df)

@app.route('/register', methods=['POST'])
def register():
    # Retrieve form data
    username = request.form.get('username')
    num_questions = int(request.form.get('num_questions'))
    
    # Assign a new user_id (max + 1)
    max_user_id = df['user_id'].max()
    new_user_id = max_user_id + 1

    return redirect(url_for('questionnaire', user_id=new_user_id, num_questions=num_questions))

@app.route('/questionnaire/<int:user_id>/<int:num_questions>', methods=['GET', 'POST'])
def questionnaire(user_id, num_questions):
    if request.method == 'POST':
        checked_comics = []
        for title in request.form:
            if request.form[title] == 'on':
                checked_comics.append(title)

        data_df = load_data('data1.pkl')

        new_rows = []
        for title in checked_comics:
            selected_comic = df.loc[df['title'] == title].iloc[0].copy()
            selected_comic['user_id'] = user_id
            new_rows.append(selected_comic)

        new_data_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

        # Update the user's preferences in the data.pkl file
        save_data('data1.pkl', new_data_df)
        

        session['checked_comics'] = checked_comics

        if checked_comics:
            # Redirect to the question2 route with the selected title and user_id
            return redirect(url_for('question2', user_id=user_id, anime_title=checked_comics[0]))

        # Redirect to the dashboard or another appropriate page
        return redirect(url_for('index'))

    comic_titles = df.sample(n=num_questions)['title'].tolist()
    return render_template('questionnaire.html', user_id=user_id, df=df, comic_titles=comic_titles, num_questions=num_questions)

@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        anime_choice = ast.literal_eval(str(request.form.get('anime_choice')))
        
        if anime_choice:
            user_id = int(anime_choice['user_id'])
            url_link = anime_choice['url_link']

            row = data['df'].loc[data['df']['url_link'] == url_link].iloc[0]
            row['user_id'] = user_id
            data['history'].append(row)

            df_combined = data['df'].append(pd.DataFrame(data['history']), ignore_index=True)
            models['item'].create(df_combined, 'user_id', 'title')

        else:
            data['history'] = []
            url_link = default_url

        # Check if it's a like_anime request
        if request.form.get('like_anime') == 'true':
            title = request.form.get('title')
            user_id = int(request.form.get('user_id'))

                        # Find the corresponding item in df according to the title
            item = df.loc[df['title'] == title].iloc[0].copy()
            item['user_id'] = user_id

            # Load data from data.pkl
            data_df = load_data('data1.pkl')

            # Add the liked item to the data_df
            data_df = pd.concat([data_df, pd.DataFrame([item])], ignore_index=True)

            # Save the updated data_df to data1.pkl
            save_data('data1.pkl', data_df)

            return jsonify(success=True)
        
    #combined_rec = combined_recommendations(user_id, models['pop'], models['item'], alpha=0.5)

        
    return render_template('dashboard.html', 
                           df=data['df'],
                           df2=data['df2'], 
                           user_id=user_id, 
                           history=data['history'],
                           pop_model=models['pop'],
                           is_model=models['item'],
                           user_sim_model=models['user_sim'],
                           #combined_rec=combined_rec, 
                           login=False,
                           url_link=url_link)

if __name__ == "__main__":
    # Load database
    df = load_data('data1.pkl')
    df2 = load_data('data2.pkl')
    data = {'df': df,'df2':df2}
    user_id = None


    #print(df2.info())
    #print(df.info())
    #print(df2.head(1))


    # Default URL
    default_url = 'https://www.baidu.com'

    # Load recommendation models
    pop_model = R.popularity_recommender_py()
    pop_model.create(df, 'user_id', 'title')
    pop_rec = pop_model.recommend(df.iloc[0]['user_id'])

    is_model = R.item_similarity_recommender_py(df, 'user_id', 'title')

    user_sim_model = R.user_similarity_recommender_py()
    user_sim_model.create(df, 'user_id', 'title', df2)


    # Store models in a dictionary
    models = {'pop': pop_rec, 'item': is_model, 'user_sim': user_sim_model}

    app.run(debug=True)

