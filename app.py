import streamlit as st
import prepration
import helper
import matplotlib.pyplot as plt
st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=prepration.pp(data)
    st.dataframe(df)

    user_list=df['user'].unique().tolist()
    user_list.remove('Group notification')
    user_list.sort()
    user_list.insert(0,'overall')
    user=st.sidebar.selectbox('user',user_list)
    col1, col2 = st.sidebar.columns(2)
    year_list = df['year'].unique().tolist()
    month_list = df['month'].unique().tolist()
    with col1:
        year_num = st.selectbox('year', year_list)
    with col2:
        month_num = st.selectbox('month', month_list)

    if st.sidebar.button('Show Analyzer'):
        num_messeges,num_words,num_media,emoji_df,sentiment = helper.basic(user, df)
        col1,col2=st.columns(2)
        col3, col4 = st.columns(2)
        with col1:
            st.header('Sentiments :- ')
            st.header(sentiment)
        with col2:
            st.header('Total Messeges :-')
            st.header(num_messeges)
        with col3:
            st.header('Total Word :-')
            st.header(num_words)
        with col4:
            st.header('Total Media :-')
            st.header(num_media)
        if user=='overall':
            col4, col5 = st.columns(2)
            x,df1=helper.plot(df)
            fig,ax=plt.subplots()
            with col4:
                st.header('Most Busy User')
                ax.bar(x.index,x.values,color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col5:
                st.header('User Contribution')
                st.dataframe(df1)
        col1,col2=st.columns(2)

        wordcloud,most_comman_word_df=helper.word_cloud(df,user)
        with col1:
            st.header('Comman Words :-')
            fig,ax=plt.subplots()
            ax.imshow(wordcloud)
            st.pyplot(fig)
        with col2:
            st.header('Most Comman Words  :-')

            fig,ax=plt.subplots()
            #fig.figure(figsize=(200, 200))
            ax.bar(most_comman_word_df['word'],most_comman_word_df['count'],color='red')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)
        col1,col2=st.columns(2)
        with col1:
            st.header('Emojis counts :-')
            st.dataframe(emoji_df)
        with col2:
            st.header('Yearly Messege :-')
            fig,ax=plt.subplots()
            plt.figure(figsize=(1000,500))
            ax.bar(df['year'].value_counts().index,df['year'].value_counts().values,color='#fc9003')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)
        month_df, day_df, date_df=helper.time(df,user,year_num,month_num)
        col1,col2=st.columns(2)
        with col1:
            st.header('Monthly Messeges of {year} :-'.format(year=year_num))
            fig, ax = plt.subplots()
            ax.bar(month_df['month'],month_df['messege'], color='#fc9003')
            plt.xticks(rotation='vertical')
            plt.xlabel(year_num)
            st.pyplot(fig)
        with col2:
            st.header('day Messeges of {month}:-'.format(month=month_num))
            fig, ax = plt.subplots()
            ax.bar(day_df['day'], day_df['messege'], color='#81f542')
            plt.xticks(rotation='vertical')
            plt.xlabel(month_num)
            st.pyplot(fig)