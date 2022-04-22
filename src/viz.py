#!/usr/bin/env python
# coding: utf-8

# Import of required libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap

# df = pd.read_csv('path/to/toyota.csv')

def clean_url(string):
    """
    input: URL (str)
    output: URL cleaned (str)
    to avoid long urls, unreadable on the display
    """
    if string is not None and type(string)==str:
        if 'honda' in string:
            return string.replace('https://brand1.fr/cars/new/', '')
        elif 'audi' in string:
            return string.replace('https://www.brand2.fr/fr/web/fr/', '')
        elif 'toyota' in string:
            return string.replace('https://www.brand3.fr/', '')
        elif 'cupra' in string:
            url = string.split('?')[0]
            return url.replace('https://www.brand4.fr/', '')
        elif 'volkswagen' in string:
            if 'utilitaires' in string:
                return string.replace('https://www.brand5.fr/', '')
            else:
                return string.replace('https://www.brand6.fr/', '')
        elif 'skoda' in string:
            return string.replace('https://www.brand7', '')
        elif 'seat' in string:
            return string.replace('https://www.brand8', '')
    else:
        return None

# df['url'] = df['url'].apply(clean_url)

def get_url_distrib(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the URL distribution in the DataFrame
    """
    fig, ax = plt.subplots()
    title = 'Distribution des URL '+brand.capitalize()+' les plus fréquentées (et ayant abouties à une conversation)'
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="url", data=df, order=df.url.value_counts()[:5].index, ax=ax).set_title(title)
    # plt.savefig("../output/"+brand+"_countplot_url.png")
    return fig

def get_url_test_distrib(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the URL distribution in the DataFrame with legend
    """
    dic={}
    urls=list(df['url'].value_counts()[:5].index)
    for i in range(0, 5):
        dic[i]=urls[i]
    fig, ax = plt.subplots()
    title = 'Distribution des URL '+brand.capitalize()+' les plus fréquentées (et ayant abouties à une conversation)'
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="url", data=df, order=df.url.value_counts()[:5].index, ax=ax).set_title(title)
    ax.set_xticklabels([i for i in range(1, 6)])
    for i in range(0, 5):
        ax.text(0.5, -0.1-i*0.05,str(i+1)+' : '+dic[i], horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
    # plt.savefig("../output/"+brand+"_countplot_url.png")
    return fig

# get_url_distrib()

def get_lq_distrib(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the last sentences distribution in the DataFrame
    """
    title = 'Distribution des dernières phrases les plus utilisées par les agents pour les conversations '+brand.capitalize()
    fig, ax = plt.subplots(1)
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="last", data=df, order=df['last'].value_counts()[:10].index, ax=ax).set_title(title)
    ax.set_xticklabels([textwrap.fill(e, 7) for e in df['last'].value_counts()[:10].index])
    # plt.savefig("../output/"+brand+"_countplot_last_sentences.png")
    return fig

def get_test_lq_distrib(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the lasts sentences distribution in the DataFrame with legend
    """
    dic={}
    sentences=list(df['last'].value_counts()[:10].index)
    for i in range(0, 10):
        dic[i]=sentences[i]
    title = 'Distribution des dernières phrases les plus utilisées par les agents pour les conversations '+brand.capitalize()
    fig, ax = plt.subplots(1)
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="last", data=df, order=df['last'].value_counts()[:10].index, ax=ax).set_title(title)
    ax.set_xticklabels([i for i in range(1, 11)])
    for i in range(0, 10):
        ax.text(0.5, -0.1-i*0.05,str(i+1)+' : '+dic[i], horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
    # plt.savefig("../output/"+brand+"_countplot_last_sentences.png")
    return fig

def get_test_blq_distrib(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the 'sentences before the last' distribution in the DataFrame
    """
    dic={}
    sentences=list(df['before_last'].value_counts()[:10].index)
    for i in range(0, 10):
        dic[i]=sentences[i]
    title = 'Distribution des avant-dernières phrases les plus utilisées dans les conversations '+brand.capitalize()
    fig, ax = plt.subplots(1)
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="before_last", data=df, order=df['before_last'].value_counts()[:10].index, ax=ax).set_title(title)
    ax.set_xticklabels([i for i in range(1, 11)])
    for i in range(0, 10):
        ax.text(0.5, -0.1-i*0.05,str(i+1)+' : '+dic[i], horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
    # plt.savefig("../output/"+brand+"_countplot_last_sentences.png")
    return fig

# get_lq_distrib()

def get_corpus(df):
    urls = list(df.url.value_counts()[:5].index)
    corpus = []
    for url in urls:
        cp = []
        for i in range(len(df)):
            if df.loc[i, 'url']==url:
                cp.append(df.loc[i, 'last'])
        corpus.append(cp)
    return corpus

# corpus = get_corpus(df)

from wordcloud import WordCloud
import numpy as np
from PIL import Image

def get_wordcloud_by_url(df, brand):
    corpus = get_corpus(df)
    urls = list(df.url.value_counts()[:5].index)
    exclure_mots = ['Merci', 'Bonjour', 'bonne', 'journée', 'Visitor', 'Je', 'avec', 'd', 'du', 'de', 'la', 'des', 'le', 'et', 'est', 'elle', 'une', 'en', 'que', 'aux', 'qui', 'ces', 'les', 'dans', 'sur', 'l', 'un', 'pour', 'par', 'il', 'ou', 'à', 'ce', 'a', 'sont', 'cas', 'plus', 'leur', 'se', 's', 'vous', 'au', 'c', 'aussi', 'toutes', 'autre', 'comme', 'Agent', ':', 'AppleWebKit', 'Mozilla', 'fr', 'Safari']

    mask = np.array(Image.open('../data/cloud.png'))
    mask[mask == 1] = 255

    for i in range(len(corpus)):
        wordcloud = WordCloud(colormap="twilight_shifted", background_color='white', stopwords=exclure_mots, max_words=30, mask=mask).generate(' '.join(corpus[i]))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.title(urls[i])
        plt.savefig("../output/"+brand+'_'+str(i)+"_wordcloud.png")
        plt.show();

# get_wordcloud_by_url(corpus)

def get_pm_distrib(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the hours distribution of conversations in afternoon
    """
    fig, ax = plt.subplots()
    pm = df[df.slot=='PM'].reset_index(drop=True)
    title = "Distribution des conversations "+brand.capitalize()+" en fonction de l'heure, l'après-midi ({} conversations)".format(str(len(pm)))
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="time", data=pm, order=[i for i in range(1, 13)], ax=ax).set_title(title)
    # plt.savefig("../output/"+brand+"_countplot_time_pm.png")
    return fig

# get_pm_distrib()

def get_am_distrib(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the hours distribution of conversations in morning
    """
    fig, ax = plt.subplots()
    am = df[df.slot=='AM'].reset_index(drop=True)
    title = "Distribution des conversations "+brand.capitalize()+" en fonction de l'heure, le matin ({} conversations)".format(str(len(am)))
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="time", data=am, order=[i for i in range(1, 13)], ax=ax).set_title(title)
    # plt.savefig("../output/"+brand+"_countplot_time_am.png")
    return fig

# get_am_distrib()

def get_am_bis_distrib(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the hours distribution of conversations in morning (last 6 hours)
    """
    fig, ax = plt.subplots()
    am = df[df.slot=='AM'].reset_index(drop=True)
    title = "Distribution des conversations "+brand.capitalize()+" en fonction de l'heure, le matin ({} conversations)".format(str(len(am)))
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="time", data=am, order=[i for i in range(6, 13)], ax=ax).set_title(title)
    # plt.savefig("../output/"+brand+"_countplot_time_am_bis.png")
    return fig

# get_am_bis_distrib()

def get_time_column(df):
    """
    input: a pandas DataFrame
    output: the pandas DataFrame
    creates a new column with time conversion
    """
    df['time_f']=''
    for i in range(len(df)):
        if df.loc[i, 'slot']=='AM':
            df.loc[i , 'time_f'] = df.loc[i , 'time']
        else:
            df.loc[i , 'time_f'] = df.loc[i , 'time']+12
    return df

def get_time_df(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the hours distribution of conversations
    """
    df = get_time_column(df)
    fig, ax = plt.subplots()
    title = "Distribution des conversations "+brand.capitalize()+" en fonction de l'heure ({} conversations)".format(str(len(df)))
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="time_f", data=df, order=[i for i in range(1, 25)], ax=ax).set_title(title)
    # plt.savefig("../output/"+brand+"_countplot_time.png")
    return fig

# get_time_df()

def get_interv_time_column(df):
    """
    input: a pandas DataFrame, the brand name(str)
    output: the pandas DataFrame
    creates a new column with time between intervals
    """
    df['interv_time']=''
    for i in range(len(df)):
        if df.loc[i, 'time_f']<=6:
            df.loc[i , 'interv_time'] = "0-6"
        elif df.loc[i, 'time_f']<=12:
            df.loc[i , 'interv_time'] = "6-12"
        elif df.loc[i, 'time_f']<=18:
            df.loc[i , 'interv_time'] = "12-18"
        else:
            df.loc[i , 'interv_time'] = "18-24"
    return df

def get_time_intervals(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display the hours distribution of conversations (with intervals)
    """
    df = get_interv_time_column(df)
    fig, ax = plt.subplots()
    title = "Distribution des conversations "+brand.capitalize()+" en fonction de l'heure ({} conversations)".format(str(len(df)))
    sns.set_theme(style="ticks", palette="pastel")
    sns.set(rc={'figure.figsize':(15,8)})
    plt.style.use('fivethirtyeight')
    sns.countplot(x="interv_time", data=df, order=["0-6", "6-12", "12-18", "18-24"], ax=ax).set_title(title)
    # plt.savefig("../output/"+brand+"_countplot_time_intervals.png")
    return fig

# get_time_intervals()

def get_time_distrib_by_url(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    for each url, display the hour distribution of conversations
    """
    urls = list(df.url.value_counts()[:5].index)
    for i in range(len(urls)):
        title = urls[i]
        sns.set_theme(style="ticks", palette="pastel")
        sns.set(rc={'figure.figsize':(15,8)})
        plt.style.use('fivethirtyeight')
        sns.countplot(x="time_f", data=df[df.url==urls[i]].reset_index(drop=True), order=[i for i in range(1, 25)]).set_title(title)
        plt.savefig("../output/"+brand+"_countplot_time_url_"+str(i)+".png")
        plt.figure().clear()

def get_wordcloud(df, brand):
    """
    input: a pandas DataFrame, the brand name(str)
    output: matplotlib Figure
    display wordcloud of the most used words in the last two sentences of conversations
    """
    fig, ax = plt.subplots()
    corpus = df['last'].to_list() + df['before_last'].to_list()
    corpus = [c for c in corpus if type(c)==str]
    exclure_mots = ['www', 'https', 'volkswagen', 'audi', 'toyota', 'honda', 'skoda', 'seat', 'cupra', 'Merci', 'Bonjour', 'bonne', 'journée', 'Visitor', 'Je', 'avec', 'd', 'du', 'de', 'la', 'des', 'le', 'et', 'est', 'elle', 'une', 'en', 'que', 'aux', 'qui', 'ces', 'les', 'dans', 'sur', 'l', 'un', 'pour', 'par', 'il', 'ou', 'à', 'ce', 'a', 'sont', 'cas', 'plus', 'leur', 'se', 's', 'vous', 'au', 'c', 'aussi', 'toutes', 'autre', 'comme', 'Agent', ':', 'AppleWebKit', 'Mozilla', 'fr', 'Safari']
    mask = np.array(Image.open('../data/cloud.png'))
    mask[mask == 1] = 255
    wordcloud = WordCloud(colormap="twilight_shifted", background_color='white', stopwords=exclure_mots, max_words=30, mask=mask).generate(' '.join(corpus))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title("Mots les plus fréquents dans les deux dernières phrases des conversations "+brand.capitalize()+" ({} conversations)".format(len(df)))
    #plt.savefig("../output/"+brand+'_'+str(i)+"_wordcloud.png")
    #plt.show();
    return fig