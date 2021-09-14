import re

import pymongo

conn = pymongo.MongoClient(host='127.0.0.1', port=27017)
dealHistoryConn = conn['lianjia']['deal_history']



def insert_deal_item(item):
    eleid = item['eleid']
    if dealHistoryConn.find({'_id': eleid}).count() == 0:
        item['_id'] = eleid
        dealHistoryConn.save(item)




if __name__ == '__main__':
    for date in ['2021-01','2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08']:
        rgx = re.compile(f'.*{date}.*', re.IGNORECASE)
        a = dealHistoryConn.find({'sign_time': rgx, 'sub_desc': re.compile(f'.*朝阳·北苑.*', re.IGNORECASE)})
        # a = dealHistoryConn.find({'sign_time': rgx})
        # a = dealHistoryConn.find({'sign_time': '/.*2021-02.*/',
        #                       'fans': {'$lt': 20}, 'ndiscovery': {'$lt': 5},
        #                       'at_count': 0})
        # print(a.count())
        count = a.count()
        money = 0
        for item in a:
            money += item['rent_price_trans']
        print(f"{date}, {count}, {money/count}")
