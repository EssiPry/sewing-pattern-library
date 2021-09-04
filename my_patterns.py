from db import db

def add_to_my_patterns(user_id, pattern_id):
    sql = "INSERT INTO my_patterns (user_id, pattern_id) VALUES (:user_id, :pattern_id)"
    db.session.execute(sql, {"user_id":user_id, "pattern_id":pattern_id})
    db.session.commit()
    return True

def delete_from_my_patterns(user_id, pattern_id):
    sql = "DELETE FROM my_patterns WHERE user_id=:user_id AND pattern_id=:pattern_id"
    db.session.execute(sql, {"user_id":user_id, "pattern_id":pattern_id})
    db.session.commit()
    return True

def get_my_patterns(user_id):
    sql = """SELECT P.company, P.name, P.id
             FROM patterns P, my_patterns A
             WHERE A.pattern_id = P.id AND A.user_id = :user_id"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def in_db(user_id, pattern_id):
    sql = "SELECT user_id FROM my_patterns WHERE user_id=:user_id AND pattern_id=:pattern_id"
    return db.session.execute(sql, {"user_id":user_id, "pattern_id":pattern_id}).fetchone()

def count_my_patterns(user_id):
    sql = "SELECT COUNT(pattern_id) FROM my_patterns WHERE user_id=:user_id"
    return db.session.execute(sql, {"user_id":user_id}).fetchone()[0]
