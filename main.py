# -*- coding: utf-8 -*-

from wox import Wox
import requests
import json
from itertools import chain

url = 'http://www.iciba.com/index.php?a=getWordMean&c=search&list=3'

class Iciba(Wox):

    def query(self, query):

        if query == '':
            return []

        res = requests.get(url, dict(word=query))
        res = json.loads(res.text)

        if res['errno'] != 0:
            return [
                {
                    'Title': '错误：%s' % res['errmsg'],
                    'SubTitle': 'errno：%s' % res['errno']
                }
            ]

        return list(chain(self.parseCollins(res), self.parseNetMean(res)))

    def parseNetMean(self, res):
        netmean = res['netmean']
        return chain(self.parseNet(netmean), self.parseRelatedPhrase(netmean))

    def parseNet(self, netmean):
        return (
            {
                'Title': x['exp'],
                'SubTitle': '网络释义：%s' % x['key']
            } for x in netmean['PerfectNetExp']
        )

    def parseRelatedPhrase(self, netmean):
        return (
            {
                'Title': y['exp'],
                'SubTitle': '网络释义：%s' % y['key']
            } for x in netmean['RelatedPhrase'] for y in x['list']
        )

    def parseCollins(self, res):
        if 'collins' not in res:
            return iter(())
        entries = res['collins'][0]['entry']
        return (
            {
                'Title': x['tran'] ,
                'SubTitle': '%s: %s' % (x['posp'].lower(), x['def'])
            } for x in entries
        )


if __name__ == "__main__":
    Iciba()
