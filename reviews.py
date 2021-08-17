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
    sql = "SELECT U.username, R.review, R.date FROM reviews R, users U, patterns P WHERE R.user_id=U.id AND R.pattern_id=P.id AND P.name=:name ORDER BY date"
    return db.session.execute(sql, {"name":name}).fetchall() 