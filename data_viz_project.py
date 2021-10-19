import instaloader
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt

#Insatgram scraping, datas and charts

account = "" #Your instagram account name
password = "" #Your password

instance = instaloader.Instaloader()
instance.login(user=account,passwd=password)

profile = instaloader.Profile.from_username(instance.context, account)

#Getting data and put them in a csv file

#followees = [followee.username for followee in profile.get_followees()]

#followees_info = pd.DataFrame(columns = ['username', 'userid', 'nbPost', 'nbFollowers', 'nbFollowees', 'biography'])

#for i in range (100):
#    tmp_profile = instaloader.Profile.from_username(instance.context, followees[i])
#    followees_info.loc[i] = [tmp_profile.username ,tmp_profile.userid ,tmp_profile.mediacount ,tmp_profile.followers ,tmp_profile.followees ,tmp_profile.biography]

#followees_info.to_csv (r'C:\Users\Armand\OneDrive\Bureau\Data_visualization\st_app\insta_data.csv', index = False, header=True)


#followee_sample = df['username'][32:43]
#followee_sample = followee_sample.drop(followee_sample.index[[3]])
#followee_sample.index = range(10)
#df_followee_sample_likes = pd.DataFrame()

#for i in range(len(followee_sample)):
#    tmp = instaloader.Profile.from_username(instance.context, followee_sample[i]).get_posts()
#    likes = 0
#    count = 0
#    for post in tmp:
#        likes += post.likes
#        count += 1
#    likes = likes / count
#    df_followee_sample_likes.insert(0,followee_sample[i], [likes])

#df_followee_sample_likes.to_csv(r'C:\Users\Armand\OneDrive\Bureau\Data_visualization\st_app\like_average_sample.csv', index = False, header=True)

df = pd.read_csv('insta_data.csv')
df_followee_sample_likes = pd.read_csv('like_average_sample.csv')

#1st chart
df_followers = df[['nbFollowers']][15:25]
df_followers.index = df['username'][15:25]


#2nd chart
similarities = alt.Chart(df).mark_point(filled=True).encode(
     alt.X('nbPost'),
     alt.Y('nbFollowers'),
     alt.Size('nbFollowees'),
    tooltip = [alt.Tooltip('username'),
                alt.Tooltip('nbFollowers'),
                alt.Tooltip('nbPost'),
                alt.Tooltip('nbFollowees')
            ]
).interactive()

#For the 3rd and 4th chart, we directly get data from instagram because it don't take a lot of time to get.

#3rd chart
my_posts = instaloader.Profile.from_username(instance.context, 'armand.dr').get_posts()
df_my_posts  = pd.DataFrame(columns= ['date', 'nbLikes'])
for post in my_posts:
    df_my_posts.loc[len(df_my_posts.index)] = [post.date, post.likes]

my_posts_stats = alt.Chart(df_my_posts.head(10)).mark_area(
    line={'color':'lightblue'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='white', offset=0),
               alt.GradientStop(color='lightblue', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    ),
    point=True  
).encode(
    alt.X('date:T'),
    alt.Y('nbLikes:Q'),
    tooltip = [alt.Tooltip('date'),
                alt.Tooltip('nbLikes'),  
            ]
)

#4th chart
dylan_nahi_posts = instaloader.Profile.from_username(instance.context, 'dylan_nahi99').get_posts()
df_dylan_nahi  = pd.DataFrame(columns= ['date', 'nbLikes'])

for post in dylan_nahi_posts:
    df_dylan_nahi.loc[len(df_dylan_nahi.index)] = [post.date, post.likes]

df_compare_likes = pd.DataFrame(columns= ['nbPost', 'likes','name'])

for i in range (10):
    df_compare_likes.loc[len(df_compare_likes.index)] = ['post ' + str(i + 1), df_my_posts['nbLikes'][i],'armand']
    df_compare_likes.loc[len(df_compare_likes.index)] = ['post ' + str(i + 1), df_dylan_nahi['nbLikes'][i],'dylan']

comparing_chart = alt.Chart(df_compare_likes).mark_bar().encode(
    x='sum(likes)',
    y='nbPost',
    color='name',
)

#5th chart
followees = df_followee_sample_likes.columns
data = df_followee_sample_likes.iloc[0]

explode = (0.5, 0.1, 0.1, 0.1, 0.3, 0.2, 0.1, 0.1, 0.7, 0.2)

wp = { 'linewidth' : 0.5, 'edgecolor' : "white" }
  
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d} likes)".format(pct, absolute)
  
fig, ax = plt.subplots(figsize =(6.5, 4))
wedges, texts, autotexts = ax.pie(data, autopct = lambda pct: func(pct, data),
                                  explode = explode,
                                  shadow = True,
                                  startangle = 90,
                                  wedgeprops = wp,
                                  textprops = dict(color ="black"))

ax.legend(wedges, followees, title ="Followees", loc ="center left", bbox_to_anchor =(1, 0, 0.5, 1))
  
plt.setp(autotexts, size = 6, weight ="bold")

# Streamlit part

st.set_page_config(layout="wide")

st.title('Welcome to my instagram\'s data visualization')

st.markdown('***')

st.markdown('+ ### **Some of my followees\'s statistics**')

st.write(" ")
st.write(" ")
st.write(" ")

st.bar_chart(df_followers)

st.write(" ")
st.write(" ")
st.write(" ")

st.markdown('+ ### **Similarities between my followees\'s**')

st.write(" ")
st.write(" ")
st.write(" ")

st.altair_chart(similarities, use_container_width=True)

st.write(" ")
st.write(" ")
st.write(" ")

st.markdown('+ ### **My last 10 instagram posts stats**')

st.write(" ")
st.write(" ")
st.write(" ")

st.altair_chart(my_posts_stats, use_container_width=True)

st.write(" ")
st.write(" ")
st.write(" ")

st.markdown('+ ### **Comparing with dylan_nahi_99\'s 10 lasts posts**')

st.write(" ")
st.write(" ")
st.write(" ")

st.altair_chart(comparing_chart, use_container_width=True)

st.write(" ")
st.write(" ")
st.write(" ")

st.markdown('+ ### **Comparing some of my followees likes average**')

st.write(" ")
st.write(" ")
st.write(" ")

st.pyplot(fig)
