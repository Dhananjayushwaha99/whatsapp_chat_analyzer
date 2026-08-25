from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
extract = URLExtract()
import emoji

def fetch_stats(selected_user,df):
    if selected_user != "overall":
        df=df[df['users']==selected_user]
    # 1 fetch number of message
    num_messages = df.shape[0]

     # 2 fetch number of word
    word=[]
    for message in df['messages']:
        word.extend(message.split())

    # 3 fetch number of media
    num_media_messages=df[df['messages']=="<Media omitted>\n"].shape[0]
    # 1 fetch number of links
    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))
    return num_messages, len(word),num_media_messages ,len(links)

def most_busy_user(df):
    x =df["users"].value_counts().head()
    df=round(df['users'].value_counts() / df.shape[0]*100,2).reset_index().rename(columns={'count':'percentage', "users": "name"})

    return x,df

def create_wordcloud(selected_user,df):


    f=open("stop_hinglish.txt","r")
    stopwords=f.read()
    if selected_user != "overall":
        df=df[df['users']==selected_user]
    temp = df[df["users"] != "group_notification"]
    temp = temp[temp['users'] != "<media omitted>\n"]
    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)

    wc= WordCloud(width=500, height=500,background_color="black")
    temp['message']=temp['messages'].apply(remove_stopwords)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc


def most_common_word(selected_user,df):
    f=open("stop_hinglish.txt","r")
    stopwords=f.read()
    if selected_user != "overall":
        df=df[df['users']==selected_user]
    temp = df[df["users"] != "group_notification"]
    temp = temp[temp['users'] != "<media omitted>\n"]

    words=[]

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
def emoji_helper(selected_user, df):
    if selected_user != "overall":
        df = df[df['users'] == selected_user]

    emojis = []

    for message in df['messages']:
        emojis.extend([item['emoji'] for item in emoji.emoji_list(message)])

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common()
    )

    return emoji_df
#
# def emoji_helper(selected_user, df):
#     if selected_user != "overall":
#         df = df[df['users'] == selected_user]
#
#     emojis = []
#
#     for message in df['messages']:
#         emojis.extend([c for c in message if emoji.is_emoji(c)])
#
#     emoji_df = pd.DataFrame(
#         Counter(emojis).most_common(len(Counter(emojis)))
#     )
#
#     return emoji_df
# #
# def emoji_helper(selected_user,df):
#     if selected_user != "overall":
#         df=df[df['users']==selected_user]
#
#     emojis=[]
#     for message in df['messages']:
#         emojis.extend([c for c in message if c in emoji.is_emoji(c)
#     emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != "overall":
        df =df[df['users']==selected_user]

    timeline = df.groupby(["year","month_num",'month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-" + str(timeline['year'][i]))
    timeline['time']= time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != "overall":
        df=df[df['users']==selected_user]
    daily_timeline=df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != "overall":
        df=df[df['users']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != "overall":
        df=df[df['users']==selected_user]
    return df['day_name'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != "overall":
        df=df[df['users']==selected_user]
    user_heatmap = df.pivot_table(index="day_name", columns="period", values="messages",aggfunc='count').fillna(0)
    return user_heatmap
