from db import db
from flask import session

def add_pattern_to_db(name, company, fabric):
    try: 
        sql = "INSERT INTO patterns (name, company, fabric) VALUES (:name, :company, :fabric)"
        db.session.execute(sql, {"name":name, "company":company, "fabric":fabric})
        db.session.commit()
        return True 
    except: 
        return False 

def add_garment_type_to_pattern(pattern_id, garment_id):
    sql= "INSERT INTO garments_in_pattern (pattern_id, garment_id) VALUES (:pattern_id, :garment_id)"
    db.session.execute(sql, {"pattern_id":pattern_id, "garment_id":garment_id})
    db.session.commit()

def get_patterns(name, company, fabric): 
    sql = "SELECT P.name, P.company, P.fabric FROM patterns P WHERE P.name LIKE :name AND P.company LIKE :company AND P.fabric LIKE :fabric" 
    return db.session.execute(sql, {"name": "%"+name+"%","company":"%"+company+"%", "fabric": fabric})  

def get_pattern_by_name(name):
    sql = "SELECT P.name, P.company, P.fabric FROM patterns P WHERE name = :name"
    return db.session.execute(sql, {"name":name}).fetchone()

def count_patterns(name, company, fabric):
    sql ="SELECT COUNT(*) FROM patterns WHERE name LIKE :name AND company LIKE :company AND fabric LIKE :fabric"
    return db.session.execute(sql, {"name":"%"+name+"%", "company":"%"+company+"%", "fabric":"%"+fabric+"%"}).fetchone()[0]

def get_pattern_id(name):
    sql ="SELECT id FROM patterns WHERE name = :name"
    return db.session.execute(sql, {"name":name}).fetchone()[0]

def get_garment_id(garment):
    sql ="SELECT id FROM garments WHERE garment = :garment"
    return db.session.execute(sql, {"garment":garment}).fetchone()[0]

def get_garments(pattern_name): 
    sql = "SELECT G.garment FROM garments G, garments_in_pattern A, patterns P WHERE A.garment_id = G.id AND A.pattern_id = P.id AND P.name=:pattern_name"
    return db.session.execute(sql, {"pattern_name":pattern_name}).fetchall()

def get_garment_types(): 
    sql = "SELECT garment, id FROM garments ORDER BY id"
    return db.session.execute(sql).fetchall()