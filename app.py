
import streamlit as st
import pandas as pd


import preprocess , helper
import matplotlib.pyplot as plt

import seaborn as sns

st.sidebar.title("whatsapp chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     data=bytes_data.decode('utf-8')
     # st.text(data)
     df=preprocess.preprocess(data)
     # st.dataframe(df)

    # fetch unique users
     user_list=df['users'].unique().tolist()
     user_list.sort()
     user_list.remove("group_notificaton")

     user_list.insert(0,"overall")
     selected_user=st.sidebar.selectbox("show analysis", user_list)

     if st.sidebar.button("Show Analysis"):
         num_message,word,num_media_meassages,num_links=helper.fetch_stats(selected_user,df)
         st.title("Top statics")
         col1,col2,col3,col4 = st.columns(4)
         with col1:
          st.header("Total messages")
          st.title(num_message)
         with col2:
          st.header("Total word")
          st.title(word)
         with col3:
           st.header("Total media")
           st.title(num_media_meassages)

         with col4:
            st.header("Total links")
            st.title(num_links)

         st.title("Montly timeline")
         timeline=helper.monthly_timeline(selected_user,df)
         fig,ax=plt.subplots()
         plt.plot(timeline['time'],timeline["messages"])
         plt.xticks(rotation='vertical')
         st.pyplot(fig)

         st.title("daily_timeline")
         daily_timeline=helper.daily_timeline(selected_user,df)
         fig,ax=plt.subplots()
         ax.plot(daily_timeline['only_date'],daily_timeline["messages"])
         plt.xticks(rotation='vertical')
         st.pyplot(fig)

         # week time line
         st.title("Activity map")
         col1,col2=st.columns(2)
         with col1:
             st.header("Most busy day ")
             busy_day=helper.week_activity_map(selected_user,df)
             fig,ax=plt.subplots()
             ax.bar(busy_day.index,busy_day.values)
             st.pyplot(fig)

         with col2:
             st.header("Most busy month")
             busy_month = helper.month_activity_map(selected_user, df)
             fig, ax = plt.subplots()
             ax.bar(busy_month.index, busy_month.values)
             plt.xticks(rotation='vertical')
             st.pyplot(fig)

         st.title("weekly activity heatmap")
         user_heatmap= helper.activity_heatmap(selected_user,df)
         fig, ax= plt.subplots()
         ax=sns.heatmap(user_heatmap)
         st.pyplot(fig)
            # find the busyest user in group
         if selected_user=="overall":
            st.title("Most_busy_user")
            most_busy_user,new_df= helper.most_busy_user(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)


            with col1:

                plt.bar(most_busy_user.index, most_busy_user.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
         # word cloude
         st.title("word cloud")
         df_wc= helper.create_wordcloud(selected_user,df)
         fig,ax=plt.subplots()
         ax.imshow(df_wc)
         st.pyplot(fig)

         # most common word
         st.title("most common words")
         most_common_df=helper.most_common_word(selected_user,df)
         # st.dataframe(most_common_df)
         fig, ax =plt.subplots()

         ax.bar(most_common_df[0], most_common_df[1])
         plt.xticks(rotation='vertical')
         st.pyplot(fig)

         # emoji analysis
         emoji_df=helper.emoji_helper(selected_user,df)
         st.title("emoji analysis")
         col1,col2=st.columns(2)
         with col1:
            st.dataframe(emoji_df)
         with col2:
             fig,ax=plt.subplots()
             ax.pie(emoji_df[1],labels=emoji_df[0],autopct="%0.2f%%")
             st.pyplot(fig)