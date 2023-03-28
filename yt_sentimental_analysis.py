import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import string
import re

def clean_text(text):
    '''
    This method cleans the text by removing punctuations, numbers and double white spaces
    Returns : cleaned text
    '''
    text = text.lower()
    text = re.sub(r"[^\\\w\s]",' ',text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r"[0-9]",'',text)
    text = re.sub(r"  ",' ',text)
    text = re.sub(r"\n",' ',text)
    return text.strip()



def join_remove_stopwords(comments):
    '''
    Given the comments,  clean text and removes stopwords and return the processed text
    '''
    comments = clean_text(comments)

    stop_words = set(stopwords.words('english'))
    wnl = WordNetLemmatizer()

    word_tokens = word_tokenize(comments)
    filtered_text = [w for w in word_tokens if not w in stop_words]
    text = ' '.join([wnl.lemmatize(word) for word in filtered_text])

    return text



def sentiment_analyser(comments_file):
    df = pd.read_csv(comments_file)
    df.dropna(inplace=True)
    df['cleaned_comments'] = df.Comment.apply(join_remove_stopwords)
    sia = SentimentIntensityAnalyzer()
    df['Sentiment Scores'] = df['cleaned_comments'].apply(lambda x: sia.polarity_scores(x)['compound'])
    df['Sentiment'] = df['Sentiment Scores'].apply(lambda s: 'Positive' if s > 0 else ('Neutral' if s == 0
                                                                                       else 'Negative'))
    df.Sentiment.value_counts().plot(kind='bar')
    plt.title('Number of Comments in each sentiment')
    plt.xticks(rotation=45)
    plt.savefig('static/sa_comment.png')
    pos_df = df[df.Sentiment == 'Positive'][['Writer', 'Comment']]
    neg_df = df[df.Sentiment == 'Negative'][['Writer', 'Comment']]
    neutral_df = df[df.Sentiment == 'Neutral'][['Writer', 'Comment']]

    return pos_df, neg_df, neutral_df

