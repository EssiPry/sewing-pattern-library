from db import db

def add_review(user_id, pattern_id, review):
        sql = """INSERT INTO reviews (user_id, pattern_id, review, date)
                 VALUES (:user_id, :pattern_id, :review, NOW())"""
        db.session.execute(sql, {"user_id":user_id, "pattern_id":pattern_id, "review":review})
        db.session.commit()
        return True

def get_reviews(pattern_id):
    sql = """SELECT U.username, R.review, R.date, R.user_id, R.id
             FROM reviews R, users U
             WHERE R.user_id=U.id AND R.pattern_id=:pattern_id ORDER BY date"""
    return db.session.execute(sql, {"pattern_id":pattern_id}).fetchall()

def delete_review(review_id):
    sql = "DELETE FROM reviews WHERE id=:review_id"
    db.session.execute(sql, {"review_id":review_id})
    db.session.commit()
    return True

def count_reviews():
    sql = "SELECT COUNT(review) FROM reviews"
    return db.session.execute(sql).fetchone()[0]

def count_reviewers():
    sql = "SELECT COUNT(DISTINCT user_id) FROM reviews"
    return db.session.execute(sql).fetchone()[0]

def top_three_reviewed():
    sql = """SELECT P.name, count(P.id) maximum
    FROM reviews R LEFT JOIN patterns P ON R.pattern_id=P.id
    GROUP BY P.name ORDER BY maximum DESC LIMIT 3"""
    return db.session.execute(sql).fetchall()
