import numpy as np
import pandas
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class user_similarity_recommender_py():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.df2 = None
        self.user_similarity_matrix = None
        self.N = 10  # Number of similar users to consider for recommendation

    def create(self, train_data, user_id, item_id, df2):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id
        self.df2 = df2
        self.user_similarity_matrix = self.calculate_user_similarity_matrix()

    def calculate_user_similarity_matrix(self):
        user_item_pivot = self.df2.pivot_table(index=self.user_id, columns=self.item_id, values='rating', fill_value=0)
        user_similarity_matrix = cosine_similarity(user_item_pivot)
        return user_similarity_matrix

    def recommend(self, target_user_id):
        similar_users = self.find_top_similar_users(target_user_id)
        recommended_items = self.get_recommended_items(target_user_id, similar_users)
        recommended_items['Rank'] = range(1, len(recommended_items) + 1)  # Add ranking
        return recommended_items


    def find_top_similar_users(self, target_user_id):
        user_similarities = self.user_similarity_matrix[target_user_id - 1]  # Assuming user_id starts from 1
        top_similar_users = user_similarities.argsort()[::-1][:self.N]
        return top_similar_users

    def get_recommended_items(self, target_user_id, similar_users):
        target_user_rated_items = set(self.df2[self.df2[self.user_id] == target_user_id][self.item_id])
        recommended_items = []
        for user in similar_users:
            user_items = set(self.df2[self.df2[self.user_id] == user + 1][self.item_id])
            items_to_recommend = user_items - target_user_rated_items
            for item in items_to_recommend:
                item_rows = self.train_data[self.train_data[self.item_id] == item]
                if not item_rows.empty:
                    item_info = item_rows.iloc[0]
                    recommended_items.append(item_info)
        recommended_items_df = pd.DataFrame(recommended_items).drop_duplicates().head(10)
        return recommended_items_df



class popularity_recommender_py():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.popularity_recommendations = None
        
    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id
        train_data_grouped = train_data.groupby([self.item_id]).agg({self.user_id: 'count'}).reset_index()
        train_data_grouped.rename(columns = {'user_id': 'score'}, inplace=True)
        train_data_sort = train_data_grouped.sort_values(['score', self.item_id], ascending = [0, 1])
        train_data_sort['Rank'] = train_data_sort['score'].rank(ascending=0, method='first')
        
        self.popularity_recommendations = train_data_sort.head(10)

    def recommend(self, user_id):    
        user_recommendations = self.popularity_recommendations
        user_recommendations['user_id'] = user_id
        cols = user_recommendations.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        user_recommendations = user_recommendations[cols]
        
        return user_recommendations

class item_similarity_recommender_py():
    def __init__(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id
        self.cooccurence_matrix = None
        self.animes_dict = None
        self.rev_animes_dict = None
        self.item_similarity_recommendations = None
        
    def get_user_items(self, user):
        user_data = self.train_data[self.train_data[self.user_id] == user]
        user_items = list(user_data[self.item_id].unique())
        
        return user_items
        
    def get_item_users(self, item):
        item_data = self.train_data[self.train_data[self.item_id] == item]
        item_users = set(item_data[self.user_id].unique())
            
        return item_users
        
    def get_all_items_train_data(self):
        all_items = list(self.train_data[self.item_id].unique())
            
        return all_items
        
    def construct_cooccurence_matrix(self, user_animes, all_animes):
        user_animes_users = []        
        for i in range(0, len(user_animes)):
            user_animes_users.append(self.get_item_users(user_animes[i]))
        cooccurence_matrix = np.matrix(np.zeros(shape=(len(user_animes), len(all_animes))), float)
           
        for i in range(0, len(all_animes)):
            animes_i_data = self.train_data[self.train_data[self.item_id] == all_animes[i]]
            users_i = set(animes_i_data[self.user_id].unique())
            
            for j in range(0, len(user_animes)):       
                users_j = user_animes_users[j]
                    
                users_intersection = users_i.intersection(users_j)
                
                if len(users_intersection) != 0:
                    users_union = users_i.union(users_j)
                    
                    cooccurence_matrix[j, i] = float(len(users_intersection)) / float(len(users_union))
                else:
                    cooccurence_matrix[j, i] = 0
                    
        
        return cooccurence_matrix

    def generate_top_recommendations(self, user, cooccurence_matrix, all_animes, user_animes):
        user_sim_scores = cooccurence_matrix.sum(axis=0) / float(cooccurence_matrix.shape[0])
        user_sim_scores = np.array(user_sim_scores)[0].tolist()

        sort_index = sorted(((e, i) for i, e in enumerate(list(user_sim_scores))), reverse=True)
        columns = ['user_id', 'anime', 'score', 'rank', 'url_link']
        df = pandas.DataFrame(columns=columns)
        rank = 1
        for i in range(0, len(sort_index)):
            if ~np.isnan(sort_index[i][0]) and all_animes[sort_index[i][1]] not in user_animes and rank <= 10:
                df.loc[len(df)] = [user, all_animes[sort_index[i][1]], sort_index[i][0], rank, self.train_data.loc[self.train_data['title'] == all_animes[sort_index[i][1]], 'url_link'].iloc[0]]
                rank = rank + 1
        if df.shape[0] == 0:
            return -1
        else:
            return df

    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

    def recommend(self, user):
        user_animes = self.get_user_items(user)
        all_animes = self.get_all_items_train_data()
        cooccurence_matrix = self.construct_cooccurence_matrix(user_animes, all_animes)
        df_recommendations = self.generate_top_recommendations(user, cooccurence_matrix, all_animes, user_animes)
        return df_recommendations

    def get_similar_items(self, item_list):
        user_animes = item_list
        all_animes = self.get_all_items_train_data()
        cooccurence_matrix = self.construct_cooccurence_matrix(user_animes, all_animes)
        user = ""
        df_recommendations = self.generate_top_recommendations(user, cooccurence_matrix, all_animes, user_animes)

        return df_recommendations
    

class combined_recommender():
    def __init__(self, popularity_model, item_similarity_model):
        self.popularity_model = popularity_model
        self.item_similarity_model = item_similarity_model

    def recommend(self, user_id):
        pop_recommendations = self.popularity_model.recommend(user_id)
        item_similarity_recommendations = self.item_similarity_model.recommend(user_id)

        combined_recommendations = pop_recommendations.merge(item_similarity_recommendations, on='anime', suffixes=('_pop', '_item_sim'))
        combined_recommendations['combined_score'] = combined_recommendations['score_pop'] + combined_recommendations['score_item_sim']
        combined_recommendations = combined_recommendations.sort_values('combined_score', ascending=False).head(10)
        combined_recommendations['Rank'] = range(1, len(combined_recommendations) + 1)
        combined_recommendations = combined_recommendations[['user_id', 'anime', 'combined_score', 'Rank']]

        return combined_recommendations

    
