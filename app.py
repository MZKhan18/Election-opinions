import streamlit as st
import numpy as np
import pickle
import string
# import seaborn as sns
import matplotlib.pyplot as plt
f = open('english_stopwords.txt')
stopwords = f.read()
stopwords = stopwords.split(',')
def preprocessing(text):
    text = text.lower()
    text = text.replace('@',' ')
    text = text.replace('\n', ' ')
    text = text.replace('.', ' ')
    text = text.replace('#', ' ')
    text = text.split()
    y = []
    for word in text:
        if word not in stopwords and word not in string.punctuation and word not in y:
            y.append(word)
    return " ".join(y)


congVsbjp = pickle.load(open('congVsbjp.pkl','rb'))
congVsbjpVect = pickle.load(open('congVsbjpVect.pkl','rb'))
sentiment = pickle.load(open('sentiment.pkl','rb'))
sentimentVect = pickle.load(open('sentimentVect.pkl','rb'))


label = False


st.title('Election Opinions on Twitter')


col1,col2 = st.columns(2)
data = {'BJP':20, 'Congress':20}
parties = list(data.keys())
values = list(data.values())
with col1:
    tweet = st.text_area("Enter Tweet")
    tweet = preprocessing(tweet)
    cong = -1
    results = [50]

    if st.button("Predict"):
        tweet1 = congVsbjpVect.transform([tweet])
        party = congVsbjp.predict(tweet1)[0]
        if party == 1:
            tweet2 = sentimentVect.transform([tweet])
            sent = sentiment.predict(tweet2)[0]
            if sent == 1:
                st.header("In Favour Of Congress")
                label = True
            else:
                st.header("In Favour Of BJP")
                label = False
        else:
            tweet2 = sentimentVect.transform([tweet])
            sent = sentiment.predict(tweet2)[0]
            if sent == 0:
                st.header("In Favour Of Congress")
                label = True
            else:
                st.header("In Favour Of BJP")
                label =  False

        c1,c2 = st.columns(2)
        with c1:
            if label:
                st.image('raga happy.jpg')
            else:
                st.image('raga sad.jpg')
        with c2:
            if label:
                st.image('namo sad.jpg')
            else:
                st.image('namo happy.jpg')
        if label:
            results.append(results[-1]+1)
        else:
            results.append(results[-1] - 1)

with col2:
    st.header("📊 Real-Time Opinion Share")

    congress_pct = results[-1]
    bjp_pct = 100 - congress_pct

    labels = ['Congress', 'BJP']
    sizes = [congress_pct, bjp_pct]

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    ax.set_title("Opinion Poll Distribution")

    st.pyplot(fig)

