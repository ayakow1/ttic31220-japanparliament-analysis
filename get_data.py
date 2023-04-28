# https://qiita.com/kenta1984/items/1acfddb3d920a11e6c8b
# https://qiita.com/sanskruthiya/items/8da9186f1764ae6b6e3a
import requests
import urllib.parse
import json
import csv
import datetime

def main():
    for year in years:
        # １月、２月、３月、…と月毎に収集
        for month in range(10, 12):
            # クエリパラメータ設定
            q_maximumRecords = 100
            q_from = str(datetime.date(year, month, 1))
            if month != 12:
                q_until = str(datetime.date(year, month+1, 1) - datetime.timedelta(days=1))
            else:
                q_until = str(datetime.date(year+1, 1, 1) - datetime.timedelta(days=1))

            # 一回当たりの抽出件数が最大100件のため、全体のレコード数から必要なループ回数を決定
            payload = 'from=' + q_from + '&until=' + q_until + '&maximumRecords=' + str(q_maximumRecords) + '&startRecord=1' + '&recordPacking=json'
            payload_encoded = urllib.parse.quote(payload)
            r = requests.get(base_url + payload_encoded)
            json_data = r.json()
            try:
                total_num = json_data["numberOfRecords"]
            except:
                print("クエリエラーにより取得できませんでした。")
                sys.exit()
            loop_num = int(json_data["numberOfRecords"]) // q_maximumRecords + 1

            # ループを回し、APIでデータ収集
            Records = []
            i = 0
            while i < loop_num:
                q_startRecord = 1 + i * q_maximumRecords
                payload = 'from=' + q_from + '&until=' + q_until + '&maximumRecords=' + str(q_maximumRecords) + '&startRecord=' + str(q_startRecord) + '&recordPacking=json'
                payload_encoded = urllib.parse.quote(payload)
                r = requests.get(base_url + payload_encoded)
                json_data = r.json()
                try:
                    for list in json_data['speechRecord']:
                        list_id = list['speechID']
                        list_kind = list['imageKind']
                        list_house = list['nameOfHouse']
                        list_topic = list['nameOfMeeting']
                        list_issue = list['issue']
                        list_date = list['date']
                        list_order = list['speechOrder']
                        list_speaker = list['speaker']
                        list_group = list['speakerGroup']
                        list_position = list['speakerPosition']
                        list_role = list['speakerRole']
                        list_speech = list['speech'].replace('\r\n', ' ').replace('\n', ' ') #発言内容の文中には改行コードが含まれるため、これを半角スペースに置換
                        list_url01 = list['speechURL']
                        list_url02 = list['meetingURL']
                        Records.append([list_id, list_kind, list_house, list_topic, list_issue, list_date, list_order, list_speaker, list_group, list_position, list_role, list_speech, list_url01, list_url02])
                    print(i)
                except:
                    print("skip")

                i += 1

            #CSVへの書き出し
            with open(str(year)+"/kokkai_speech_" + str(year) + str(month) + ".csv", 'w', newline='') as f:
                csvwriter = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC) #CSVの書き出し方式を適宜指定
                csvwriter.writerow(['発言ID', '種別', '院名', '会議名', '号数', '日付', '発言番号', '発言者名', '発言者所属会派', '発言者肩書き', '発言者役割', '発言内容', '発言URL', '会議録URL'])
                for record in Records:
                    csvwriter.writerow(record)


if __name__ == "__main__":
    base_url = 'http://kokkai.ndl.go.jp/api/1.0/speech?'
    years = [2010] 

    main()