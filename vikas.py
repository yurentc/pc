
from vika import Vika
import datetime
import pytz
from threading import Thread
import json

class VikaTable:
    def __init__(self):
        self.api='uskpn2kit9DR4MLd1LOc7ES'
        self.sheet='dstTlft0ZxBxb16Hw6'
        self.viewid='viw0lTqyhAHlD'
        self.vika = Vika(self.api)
        self.datasheet = self.vika.datasheet(self.sheet)

    def upsert_record(self, fields):
        records = self.datasheet.records.filter(题号=fields['题号'])
        now = datetime.datetime.now()
        year, week, days = now.isocalendar()
        if records:
            复习时间 = int(datetime.datetime.strptime(fields['复习时间'], '%Y-%m-%d').replace(tzinfo=pytz.utc).timestamp() * 1000)

            record = self.datasheet.records.get(题号=fields['题号'])
            历史记录=record.json()
            print(历史记录)
            历史记录=历史记录["历史记录"]
            历史记录=str(历史记录)+","+"\n"+str(fields['次'])+":"+str(year)+'-'+str(week)+'-'+str(days)
            records[0].update({
                "次": int(fields['次']),
                "复习时间": 复习时间,
                "历史记录": 历史记录
            })
        else:
            复习时间 = int(datetime.datetime.strptime(fields['复习时间'], '%Y-%m-%d').replace(tzinfo=pytz.utc).timestamp() * 1000)
            开始时间 = int(datetime.datetime.strptime(fields['开始时间'], '%Y-%m-%d').replace(tzinfo=pytz.utc).timestamp() * 1000)

            网址={
                "title": fields['网址'],
                "text": fields['题目'],
                "favicon": ""
            }
            历史记录="1:"+str(year)+'-'+str(week)+'-'+str(days)
            self.datasheet.records.create({
                "题号": fields['题号'],
                "题目": fields['题目'],
                "开始时间": 开始时间,
                "次": int(fields['次']),
                "复习时间": 复习时间,
                "网址": fields['网址'],
                "日志": 网址,
                "历史记录": str(历史记录)
            })

    def upsert_record_thread(self, fields):
        t = Thread(target=self.upsert_record, args=(fields,))
        t.start()

    def get_record_by_id(self, id):
        record = self.datasheet.records.get(题号=id)
        if not record:
            return None
        return record.json()

    def get_all(self):
        records = self.datasheet.records.all(viewid=self.viewid)
        return records


    def shijiancuo_to_time(ts):
        return str(datetime.datetime.fromtimestamp(int(ts)/ 1000).strftime('%Y-%m-%d'))

    def time_to_shijiancuo(ts):
        utc_timestamp = int(datetime.datetime.strptime(ts, '%Y-%m-%d').replace(tzinfo=pytz.utc).timestamp() * 1000)
        return utc_timestamp