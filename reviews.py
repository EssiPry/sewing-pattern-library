from db import db

def add_review(user_id, pattern_id, review):
    try:
        sql = """INSERT INTO reviews (user_id, pattern_id, review, date)
                 VALUES (:user_id, :pattern_id, :review, NOW())"""
        db.session.execute(sql, {"user_id":user_id, "pattern_id":pattern_id, "review":review})
        db.session.commit()
        return True
    except:
        return False

def get_reviews(pattern_id):
    sql = """SELECT U.username, R.review, R.date
             FROM reviews R, users U
             WHERE R.user_id=U.id AND R.pattern_id=:pattern_id ORDER BY date"""
    return db.session.execute(sql, {"pattern_id":pattern_id}).fetchall()

def count_reviews():
    sql="SELECT COUNT(review) FROM reviews"
    return db.session.execute(sql).fetchone()[0]

def count_reviewers():
    sql="SELECT COUNT(DISTINCT user_id) FROM reviews"
    return db.session.execute(sql).fetchone()[0]
