import requests
import json
key = "mykey"
v_api = "5.71"
def check_valid_date(data):
    data = data.split('.')
    try:
        return data[2]
    except IndexError:
        return None
def calc_age(uid):
    res = {}
    ans = requests.get(f"https://api.vk.com/method/users.get?user_ids={uid}&access_token={key}&v={v_api}")
    data = json.loads(ans.text)
    id_user = data['response'][0]['id']
    ans1 = requests.get(f"https://api.vk.com/method/friends.get?v={v_api}&access_token={key}&user_id={id_user}&fields=bdate")
    data1 = json.loads(ans1.text)
    friends_info = data1['response']['items']
    #print(friends_info)
    for obj in friends_info:
        if 'bdate' in obj:
            year = check_valid_date(obj['bdate'])
            if year:
                age = 2020 - int(year)
                res[age] = res.get(age,0) + 1
            else:
                continue
    l = []

    for k, v in res.items():
        l.append((k, v))
    l.sort(key=lambda tup: tup[0])
    l.sort(key = lambda tup :tup[1],reverse=True)
    return l

if __name__ == '__main__':
    res = calc_age('you_name_or_id')
