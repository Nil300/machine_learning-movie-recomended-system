import flask
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from tmdbv3api import TMDb
# from tmdbv3api import Movie

app = flask.Flask( __name__, template_folder='templates' )

# tmdb = TMDb()
# tmdb.api_key = '69475be7c4bc9efb7b34bcdf0ee27a50'
# tmdb.language = 'en'
# tmdb.debug = True
df2 = pd.read_csv( './model/final_data.csv' )

count = CountVectorizer( stop_words='english' )
count_matrix = count.fit_transform( df2['comb'] )

cosine_sim2 = cosine_similarity( count_matrix, count_matrix )

df2 = df2.reset_index()
indices = pd.Series( df2.index, index=df2['movie_title'] )
all_titles = [df2['movie_title'][i] for i in range( len( df2['movie_title'] ) )]

# movie = Movie()

# def get_input_image(title):
#
#     title = title.title()
#     search = movie.search( title )
#     for res in search:
#         if res.title == title:
#             movie_id = res.id
#             movie_image = res.poster_path
#             movie_actors = movie.credits( res.id )
#     return (movie_id, movie_image, movie_actors)


def get_recommendations(title):
    # cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list( enumerate( cosine_sim2[idx] ) )
    sim_scores = sorted( sim_scores, key=lambda x: x[1], reverse=True )
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    title = df2['movie_title'].iloc[movie_indices]
    direct = df2['director_name'].iloc[movie_indices]
    actor_1 = df2['actor_1_name'].iloc[movie_indices]
    actor_2 = df2['actor_2_name'].iloc[movie_indices]
    actor_3 = df2['actor_3_name'].iloc[movie_indices]
    return_df = pd.DataFrame( columns=['Movie Title', 'Director Name', 'Actor 1', 'Actor 2', 'Actor 3'] )
    return_df['Movie Title'] = title
    return_df['Director Name'] = direct
    return_df['Actor 1'] = actor_1
    return_df['Actor 2'] = actor_2
    return_df['Actor 3'] = actor_3
    return return_df


# Set up the main route
@app.route( '/', methods=['GET', 'POST'] )
def main():
    if flask.request.method == 'GET':
        return flask.render_template( 'index.html' )

    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
        m_name = m_name.lower()
        if m_name not in all_titles:
            return flask.render_template( 'negative.html', name=m_name )
        else:
            # img_actor_result = get_input_image(m_name)
            # input_movie_id =img_actor_result[0]
            # input_movie_image_link = img_actor_result[1]
            # input_movie_crew_cast = img_actor_result[2]
            # actor_one = input_movie_crew_cast.cast[0]['name']
            # actor_one_img_link = input_movie_crew_cast.cast[0]['profile_path']
            # actor_two = input_movie_crew_cast.cast[1]['name']
            # actor_two_img_link = input_movie_crew_cast.cast[1]['profile_path']
            # actor_three = input_movie_crew_cast.cast[2]['name']
            # actor_three_img_link = input_movie_crew_cast.cast[2]['profile_path']
            # director_name = input_movie_crew_cast.crew[0]['name']
            # director_img_link = input_movie_crew_cast.crew[0]['profile_path']
            # bas_img = 'https://image.tmdb.org/t/p/w500'
            # input_movie_image = bas_img + input_movie_image_link
            # actor_one_img = bas_img + actor_one_img_link
            # actor_two_img = bas_img + actor_two_img_link
            # actor_three_img = bas_img + actor_three_img_link
            # director_img = bas_img + director_img_link

            result_final = get_recommendations( m_name )

            names = []
            direct_name = []
            actor_1_name = []
            actor_2_name = []
            actor_3_name = []
            for i in range( len( result_final ) ):
                names.append( result_final.iloc[i][0] )
                direct_name.append( result_final.iloc[i][1] )
                actor_1_name.append( result_final.iloc[i][2] )
                actor_2_name.append( result_final.iloc[i][3] )
                actor_3_name.append( result_final.iloc[i][4] )

            # recommend_movie_list = []
            # for idnum in result_final:
            #     recommend_movie_list.append( idnum )
            #
            #
            # input_res_image = []
            #
            # for i in recommend_movie_list:
            #     search = movie.search( i.title() )
            #     for res in search:
            #         if res.title == i.title():
            #             input_res_image.append( res.poster_path )
            #
            # rec_movie_1_link = input_res_image[0]
            # rec_movie_2_link = input_res_image[1]
            # rec_movie_3_link = input_res_image[2]
            # rec_movie_4_link = input_res_image[3]
            # rec_movie_5_link = input_res_image[4]
            # rec_movie_6_link = input_res_image[5]
            # rec_movie_7_link = input_res_image[6]
            # rec_movie_8_link = input_res_image[7]
            # rec_movie_9_link = input_res_image[8]
            # rec_movie_10_link = input_res_image[9]
            #
            # rec_movie_1_img = bas_img + rec_movie_1_link
            # rec_movie_2_img = bas_img + rec_movie_2_link
            # rec_movie_3_img = bas_img + rec_movie_3_link
            # rec_movie_4_img = bas_img + rec_movie_4_link
            # rec_movie_5_img = bas_img + rec_movie_5_link
            # rec_movie_6_img = bas_img + rec_movie_6_link
            # rec_movie_7_img = bas_img + rec_movie_7_link
            # rec_movie_8_img = bas_img + rec_movie_8_link
            # rec_movie_9_img = bas_img + rec_movie_9_link
            # rec_movie_10_img = bas_img + rec_movie_10_link

            return flask.render_template( 'positive.html',
                                          # movie_img=input_movie_image, movie_ac_1=actor_one,
                                          # movie_ac_1_img=actor_one_img, movie_ac_2=actor_two, movie_ac_2_img=actor_two_img,
                                          # movie_ac_3=actor_three, movie_ac_3_img=actor_three_img,
                                          # movie_director =director_name, movie_director_img=director_img,
                                          movie_names=names, movie_direct=direct_name,
                                          movie_actor_one=actor_1_name, movie_actor_two=actor_2_name,
                                          movie_actor_three=actor_3_name,
                                          # recommend_movie_imgs_1 = rec_movie_1_img,
                                          # recommend_movie_imgs_2=rec_movie_2_img,recommend_movie_imgs_3 = rec_movie_3_img,
                                          # recommend_movie_imgs_4=rec_movie_4_img,recommend_movie_imgs_5 = rec_movie_5_img,
                                          # recommend_movie_imgs_6=rec_movie_6_img,recommend_movie_imgs_7 = rec_movie_7_img,
                                          # recommend_movie_imgs_8=rec_movie_8_img,recommend_movie_imgs_9 = rec_movie_9_img,
                                          # recommend_movie_imgs_10=rec_movie_10_img,bas_link = bas_img,
                                          search_name=m_name.title())


if __name__ == '__main__':
    app.run()
