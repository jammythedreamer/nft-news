import json
import requests
import time
import os
from bs4 import BeautifulSoup

if __name__ == '__main__':

    # slack_token = os.environ.get('SLACK_BOT_TOKEN')
    slack_token = ""

    channelName = "nft-news"

    channel_id = "C022LMY3EQL"

    double_quote = "\""

    json_slack_path = "./data.json"

    while True:
        req = requests.get("https://www.coindeskkorea.com/news/articleList.html?sc_area=A&view_type=sm&sc_word=nft&sc_order_by=E&sc_sdate=&sc_edate=")
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find("section", {"class": "article-list-content type-sm text-left"})
        post_idx = str(posts.find("div", {"class": "list-titles"}).a).split("idxno=")[1].split(double_quote)[0]

        with open(json_slack_path, 'r') as json_file:
            data_dick = json.load(json_file)
        last_idx = data_dick["LAST_IDX"]

        if last_idx == post_idx:
            continue

        last_idx = post_idx

        data_dick["LAST_IDX"] = last_idx
        with open(json_slack_path, 'w') as json_file:
            data_string = json.dumps(data_dick)
            json_file.write(data_string)

        message = [
            {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'{posts.find("div", {"class": "list-titles"}).text}'
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Click Me",
                            "emoji": True
                        },
                        "value": "click_me_123",
                        "url": f'https://coindeskkorea.com{str(posts.find("div", {"class": "list-titles"}).a).split(double_quote)[1]}',
                        "action_id": "button-action"
                    }
            }
        ]

        data = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': slack_token,
            'channel': channel_id,
            'blocks': json.dumps(message),
        }

        URL = 'https://slack.com/api/chat.postMessage'
        res = requests.post(URL, data= data)
        time.sleep(60)
