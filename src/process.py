# Import of required libraries
import zenpy
import pandas as pd
import re
from datetime import datetime
from viz import *
import os
import yaml
import logging
import streamlit as st
import time
from connection import *

# FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
logging.basicConfig(level=logging.INFO)

def intersection(lst1, lst2):
    """
    input: two lists
    output: a list
    returns in the list the intersection between two lists (common terms)
    """
    return list(set(lst1) & set(lst2))

def get_url(zenpy_client, tid):
    """
    input: a Zenpy's ticket id (str)
    output: the URL (str)
    scans the ticket information and returns the URL where the visitor was
    """
    for comment in zenpy_client.tickets.comments(ticket=tid):
        lines = comment.body.split('\n')
        for line in lines:
            elems = line.split(': ')
            if elems[0]=='URL':
                return elems[1]

def get_lasts(zenpy_client, tid):
    """
    input: a Zenpy's ticket id
    output: a list with two occurences in str format
    returns a list with, first, the last sentence of the conversation and then the sentence before
    """
    detect_last = detect_before = False
    msgs = []
    res = []
    for comment in zenpy_client.tickets.comments(ticket=tid):
        lines = comment.body.split('\n')
        for line in lines:
            if '(' in line and '*' not in line:
                msgs.append(line)
    if msgs:
        last = msgs[len(msgs)-1]
        before = msgs[len(msgs)-2]
        for val in (last, before):
            if 'Visitor' in val:
                val = re.sub("[\(\[].*?[\)\]]", "", val)
                val = val.strip()
                val = val.split(':')
                val[0]='Visitor'
                val = ':'.join(val)
            else:
                val = re.sub("[\(\[].*?[\)\]]", "", val)
                val = val.strip()
                val = val.split(':')
                val[0] = 'Agent'
                val = ':'.join(val)
            res.append(val)
    else:
        res = [None, None]
    return res

def process_period(zenpy_client, bids: list, month: int, year: int, my_bar):
    """
    :param bids: list of brand_ids we need to process
    :param month: month to process
    :param year: year to process
    :return: ultimately Dataframe with a loading progress bar in the function for the streamit application
    """
    # df = pd.DataFrame(columns=["cid", "tid", "time", "slot", "before_last", "last", "status", "device", "type_device", "os", "browser"])
    df = pd.DataFrame(columns=["tid", "created", "status", "time", "slot", "url", "last", "before_last"])
    query = "brand_id:{bid}"
    it = 0
    total = 1
    for bid in bids:
        logging.info("processing ", bid)
        for ticket in zenpy_client.search(query.format(bid=str(bid)), type='ticket', sort_by='created_at',
                                          sort_order='desc')[:999]:
            ticket_data = ticket.__dict__
            tid = ticket_data['id']
            created = ticket_data['created_at']
            status = ticket_data["status"]
            dt = datetime.strptime(ticket_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            total += 1
            if dt.month == month and dt.year == year:
                tid = ticket_data['id']
                dt_2 = dt.strftime("%I:%M %p")
                time = dt_2.split(':')[0]
                slot = dt_2.split(' ')[1]
                url = get_url(zenpy_client, tid)
                lasts = get_lasts(zenpy_client, tid)
                df.loc[len(df)] = [tid, created, status, int(time), slot, url, lasts[0], lasts[1]]
                it+=1
                logging.info('Added {} lines out of 999 possible!'.format(str(it)))
                if total!=999:
                    my_bar.progress(it/999)
                else:
                    my_bar.progress(1.0)

    # output_file = '../data/{}_{}_{}.csv'.format(str(bids), month, year)
    # df.to_csv(output_file, index=False)
    # logging.info("CSV file generated in data folder, path : {}".format())
    return df

def dataviz(df, brand):
    """
    input: a pandas DataFrame and the brand (str)
    produces the data visualisations
    """
    logging.info("Start of dataviz generation!")
    # df = pd.read_csv(filename)
    df['url'] = df['url'].apply(clean_url)
    get_url_distrib(df, brand)
    plt.clf()
    get_lq_distrib(df, brand)
    plt.clf()
    corpus = get_corpus(df)
    get_wordcloud_by_url(df, corpus, brand)
    plt.clf()
    get_pm_distrib(df, brand)
    plt.clf()
    get_am_distrib(df, brand)
    plt.clf()
    get_am_bis_distrib(df, brand)
    plt.clf()
    df = get_time_column(df)
    get_time_df(df, brand)
    plt.clf()
    df = get_interv_time_column(df)
    get_time_intervals(df, brand)
    plt.clf()
    get_time_distrib_by_url(df, brand)
    logging.info("Dataviz successfully generated in the output folder!")
    logging.info('End of the process')
