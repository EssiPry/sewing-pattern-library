from db import db

def add_to_my_patterns(user_id, pattern_id):
    try:
        sql = "INSERT INTO my_patterns (user_id, pattern_id) VALUES (:user_id, :pattern_id)"
        db.session.execute(sql, {"user_id":user_id, "pattern_id":pattern_id})
        db.session.commit()
        return True
    except:
        return False
