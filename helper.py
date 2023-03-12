from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import numpy as np
import emoji
from textblob import TextBlob
def basic(user_list,df):
    if user_list != 'overall':
        new_df = df[df['user']==user_list]
    else:
        new_df=df
    new_df['sentiment'] = new_df['messege'].apply(lambda x: TextBlob(x).sentiment.polarity)
    a = new_df['sentiment'].mean()
    if (-1 < a <= -0.5):
        sentiment = 'Negitive'
    elif ((-0.5) < a < (-0.1)):
        sentiment = 'Slightly Negative'
    elif (-0.1 < a < 0.1):
        sentiment = 'Neutral'
    elif (0.1 <= a < 0.5):
        sentiment = 'Slightly Positive'
    else:
        b = 'Positive'
    new_df=new_df.drop(columns=['sentiment'])
    num_messege = new_df.shape[0]
    emoj = pd.DataFrame(emoji.EMOJI_DATA)

    L = np.transpose(emoj).index

    emojis = []
    for i in new_df['messege']:
        emojis.extend(x for x in i if x in L)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))
    emoji_df = emoji_df.rename(columns={0: 'emojis', 1: 'count'})

    def num_word(df):
        a = 0
        for i in range(0, len(df)):
            a = a + len(df['messege'].iloc[i].split())
        return a
    num_words=num_word(new_df)
    num_media=len(new_df[new_df['messege']==' <Media omitted>'])
    return num_messege,num_words,num_media,emoji_df,sentiment
def plot(df):
    A=round((df['user'].value_counts()/len(df))*100,2).reset_index().rename(columns={'index':'name','user':'percent(%)'})
    return df['user'].value_counts().head(),A
def word_cloud(df,user):
    if user=='overall':
        new_df = df[(df['user'] != 'Group notification')]
        new_df = new_df[df['messege'] != ' <Media omitted>']
    else:
        new_df=df[(df['user']==user)]
        new_df = new_df[df['messege'] != ' <Media omitted>']
    def wording(x):
        x = x.lower()
        x = word_tokenize(x)
        y = []
        for i in x:
            if i not in stopwords.words('english'):
                if i not in '!"#$%&\'()*+,-./:;<=>[\\]^_`{|}~':
                    i = PorterStemmer().stem(i)
                    y.append(i)
        return ' '.join(y)

    new_df['messege'] = new_df['messege'].apply(lambda x:wording(x))
    def token(x):
        y=[]
        for i in x['messege']:
            y.extend(word_tokenize(i))
        return y
    A=pd.DataFrame(Counter(token(new_df)).most_common(20))
    A.rename(columns={0: 'word', 1: "count"}, inplace=True)
    wordcloud = WordCloud(width=500, height=500,
                          background_color='white',
                          min_font_size=10).generate(new_df['messege'].str.cat(sep=' '))
    return wordcloud,A
def time(df,user,year,month):
    if user != 'overall':
        df = df[df['user'] == user]
    else:
        df = df
    df['dates'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    time_df = pd.DataFrame(df.groupby(['year', 'month', 'month_num', 'dates']).count()['messege'].reset_index())
    time_df = time_df.sort_values('dates')

    month_df = time_df[time_df['year'] == year]
    month_df = month_df.groupby(['month', 'month_num']).sum()['messege'].reset_index().sort_values('month_num')
    time_df['dates'] = pd.to_datetime(time_df['dates'])
    date_df=time_df[time_df['month']==month]
    time_df['day'] = time_df['dates'].dt.day_name()
    day_df = time_df.groupby(['month', 'month_num', 'day']).sum()['messege'].reset_index().sort_values('month_num')
    return month_df,day_df,date_df

