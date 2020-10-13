import pandas as pd
from pymongo import MongoClient
from datetime import datetime


def get_connect(db, collection):
    client = MongoClient("mongodb://localhost:27017")
    db = client.get_database(db)
    data = db.get_collection(collection).find()
    return [i for i in data]


def count_pageviews(list):
    df = pd.DataFrame(list)
    count_pageviews = df[['totals']]
    totals = count_pageviews.totals.to_dict() # RECORD
    pageviews = pd.DataFrame(totals).T['pageviews']

    count_pageviews.drop('totals', axis='columns', inplace=True)

    count_pageviews.insert(loc=0, column='pageviews', value=pageviews)

    count_pageview = sum([int(i) if type(i) == type(str()) else 0 for i in count_pageviews['pageviews']])

    print('\n Contagem de Pageviews: ', count_pageview)


def number_sessions_by_user(list):
    df = pd.DataFrame(list)
    number_sessions_by_user = df[['fullVisitorId', 'visitId', 'totals']]
    totals = number_sessions_by_user.totals.to_dict()
    visits = pd.DataFrame(totals).T['visits']

    number_sessions_by_user.drop('totals', axis='columns', inplace=True)
    number_sessions_by_user.insert(loc=0, column='visits', value=visits)

    number_sessions_by_user_group = number_sessions_by_user.groupby(['fullVisitorId', 'visitId'])
    session_per_users_dict = {}

    for name, group in number_sessions_by_user_group:
        if not session_per_users_dict.get(name):
            session_per_users_dict.update({name:1})
        else:
            session_per_users_dict[name] = session_per_users_dict[name] + 1

    print('\n Sessões por usuário:')

    for key, value in sorted(session_per_users_dict.items(), key=lambda x: x[0]):
        print('{} fullVisitorId | {} visitId com {} sessão(ões)'.format(key[0], key[1], value))


def sessions_per_date(list):
    df = pd.DataFrame(list)
    df_with_date = df[['fullVisitorId', 'visitId', 'totals', 'date']]
    totals = df_with_date.totals.to_dict()
    visits = pd.DataFrame(totals).T['visits']

    df_with_date.drop('totals', axis='columns', inplace=True)
    df_with_date.insert(loc=0, column='visits', value=visits)

    number_sessions_by_date_group = df_with_date.groupby(['date'])

    sessions_per_date_dict = {}
    for name, group in number_sessions_by_date_group:

        date = datetime.strptime(name, '%Y%m%d').date().strftime('%d/%m/%Y')
        sessions = sum([int(i) for i in group['visits']])

        sessions_per_date_dict.update({date: sessions})

    print('\n Sessões distintas por data:')

    for key, value in sessions_per_date_dict.items():
        print('Data: {} recebeu: {} sessão(ões) distinta(s)'.format(key, value))


def avg_sessions_per_date(list):
    df = pd.DataFrame(list)
    df_with_timeOnSite = df[['fullVisitorId', 'visitId', 'totals', 'date']]
    totals = df_with_timeOnSite.totals.to_dict()
    timeOnSite = pd.DataFrame(totals).T['timeOnSite']

    df_with_timeOnSite.drop('totals', axis='columns', inplace=True)
    df_with_timeOnSite.insert(loc=0, column='timeOnSite', value=timeOnSite)

    df_with_timeOnSite_group = df_with_timeOnSite.groupby(['date'])

    sessions_per_date_dict = {}
    for name, group in df_with_timeOnSite_group:
        date = datetime.strptime(name, '%Y%m%d').date().strftime('%d/%m/%Y')
        list_timeOnSite = [int(i) if type(i) == type(str()) else 0 for i in group['timeOnSite']]
        avg_session = sum(list_timeOnSite) / len(list_timeOnSite)

        sessions_per_date_dict.update({date: avg_session})

    print('\n Média de duração da sessão por data:')

    for key, value in sessions_per_date_dict.items():
        print('Data: {} média {} segundos'.format(key,  round(value, 2)))


def sessions_per_browser(list):

    df = pd.DataFrame(list)
    df_with_device = df[['fullVisitorId', 'visitId', 'totals', 'device', 'date']]

    totals = df_with_device.totals.to_dict()
    device = df_with_device.device.to_dict()

    visits = pd.DataFrame(totals).T['visits']
    browser = pd.DataFrame(device).T['browser']


    df_with_device.drop('totals', axis='columns', inplace=True)
    df_with_device.drop('device', axis='columns', inplace=True)

    df_with_device.insert(loc=0, column='visits', value=visits)
    df_with_device.insert(loc=0, column='browser', value=browser)

    df_with_device_group = df_with_device.groupby(['browser', 'date'])

    sessions_per_device_date_dict = {}
    for name, group in df_with_device_group:

        date = datetime.strptime(name[1], '%Y%m%d').date().strftime('%d/%m/%Y')
        sessions = sum([int(i) if type(i) == type(str()) else 0 for i in group['visits']])

        sessions_per_device_date_dict.update({(date,name[0]): sessions})

    print('\n Sessões diárias por tipo de browser:')
    
    for key, value in sorted(sessions_per_device_date_dict.items(), key=lambda x: datetime.strptime(x[0][0], '%d/%m/%Y')):
        print('data-browser: {} com {} sesssão(ões)'.format(key, value))


def main():
    list = get_connect(db='dados-google-analytics', collection='analytics')

    # Contagem de Pageviews;
    count_pageviews(list)

    # Número de sessões por usuário
    number_sessions_by_user(list)

    # Sessões distintas por data;
    sessions_per_date(list)

    # Média de duração da sessão por data
    avg_sessions_per_date(list)

    # Sessões diárias por tipo de browser
    sessions_per_browser(list)

if __name__ == '__main__':
    main()
