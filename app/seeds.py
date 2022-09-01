import random
from app.models import *

def create_data():
    hobbies = [
        {"name": 'Football'},
        {"name": 'Tennis'}, 
        {"name": 'Basketball'}, 
        {"name": 'Volleyball'}, 
        {"name": 'Judo'}
    ]
    for hobby in hobbies:
        Hobby(hobby).save()

    for i in range(10):
        data = {
            "name": f"user{i}",
            "email": f"mail{i}@gmail.com",
            "password": "1234" + str(i),


        }
        
        User(data).save()

    positive_review = [
        "",
        "thank you",
        "きみは最高の友達だよ。",
        "昨日、宿題を手伝ってくれてありがとうございました", 
        "頭 いい ですね！",
        "あなたと お話 が できうれしかったです！",
        "あなた は おもしろい！ ",
        "きみをみてると、もっと自分を磨かなきゃって気持ちになります。"
    ]
    negative_review = [
        "",
        " 引き受けらえません",
        "そっちも空いていない",
        "私たちはうまくやっていけません",
        "私たちの見解は同じではありません"
    ]

    users = User.query.all()
    users_id = [ u.id for u in users]
    for i in range(40):
        from_id, to_id = random.sample(users_id, 2)
        score = random.choice(range(1,5))
        if score >=3:
            content = random.choice(positive_review)
        else:
            content = random.choice(negative_review)
        data = {
            "fk_user_from": from_id,
            "fk_user_to": to_id,
            "content": content,
            "score": score,
        }
        Review(data).save()
        if score >=3:
            content = random.choice(positive_review)
        else:
            content = random.choice(negative_review)
        data = {
            "fk_user_from": to_id,
            "fk_user_to": from_id,
            "content": content,
            "score": score,
        }
        Review(data).save()

    