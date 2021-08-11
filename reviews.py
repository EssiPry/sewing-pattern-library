from db import db
from flask import session
import users, sewingpatterns

def add_review(user_id, pattern_id, review): 
    try: 
        sql = "INSERT INTO reviews (user_id, pattern_id, review, date) VALUES (:user_id, :pattern_id, :review, NOW())"
        db.session.execute(sql, {"user_id":user_id, "pattern_id":pattern_id, "review":review})
        db.session.commit()
        return True 
    except: 
        return False 


def get_reviews(name): 
    name=name 
    sql = "SELECT review FROM reviews WHERE name = :name ORDER BY date"
    db.session.execute