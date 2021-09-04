from db import db

def add_pattern_to_db(name, company, fabric):
    try:
        sql = "INSERT INTO patterns (name, company, fabric) VALUES (:name, :company, :fabric)"
        db.session.execute(sql, {"name":name, "company":company, "fabric":fabric})
        db.session.commit()
        return True
    except:
        return False

def get_patterns(name, company, fabric, garment_id):
    if not garment_id:
        sql = """SELECT P.name, P.company, P.fabric, P.id
             FROM patterns P
             WHERE P.name LIKE :name
             AND P.company LIKE :company
             AND P.fabric LIKE :fabric"""
        return db.session.execute(
            sql, {"name": "%"+name+"%", "company":"%"+company+"%", "fabric": fabric}).fetchall()
    sql = """SELECT P.name, P.company, P.fabric, P.id
             FROM patterns P, garments_in_pattern G
             WHERE P.id = G.pattern_id
             AND P.name LIKE :name
             AND P.company LIKE :company
             AND P.fabric LIKE :fabric
             AND G.garment_id = :garment_id"""
    return db.session.execute(
        sql, {"name": "%"+name+"%", "company":"%"+company+"%", "fabric": fabric,
              "garment_id": garment_id}).fetchall()

def get_pattern_by_id(pattern_id):
    sql = "SELECT P.name, P.company, P.fabric FROM patterns P WHERE id = :pattern_id"
    return db.session.execute(sql, {"pattern_id":pattern_id}).fetchone()

def count_patterns(name, company, fabric, garment_id):
    if not garment_id:
        sql = """SELECT COUNT(id)
                 FROM patterns
                 WHERE name LIKE :name
                 AND company LIKE :company
                 AND fabric LIKE :fabric"""
        return db.session.execute(
            sql, {"name":"%"+name+"%", "company":"%"+company+"%", "fabric":"%"+fabric+"%"}
            ).fetchone()[0]
    sql = """SELECT COUNT(P.id)
             FROM patterns P, garments_in_pattern G
             WHERE P.id = G.pattern_id
             AND P.name LIKE :name
             AND P.company LIKE :company
             AND P.fabric LIKE :fabric
             AND G.garment_id = :garment_id"""
    return db.session.execute(
        sql, {"name":"%"+name+"%", "company":"%"+company+"%", "fabric":"%"+fabric+"%",
              "garment_id": garment_id}).fetchone()[0]

def get_pattern_id(name):
    sql = "SELECT id FROM patterns WHERE name = :name"
    return db.session.execute(sql, {"name":name}).fetchone()[0]

def add_garment_type_to_pattern(pattern_id, garment_id):
    sql = """INSERT INTO garments_in_pattern (pattern_id, garment_id)
             VALUES (:pattern_id, :garment_id)"""
    db.session.execute(sql, {"pattern_id":pattern_id, "garment_id":garment_id})
    db.session.commit()
    return True

def get_garment_id(garment):
    sql = "SELECT id FROM garments WHERE garment = :garment"
    return db.session.execute(sql, {"garment":garment}).fetchone()[0]

def get_garments(pattern_id):
    sql = """SELECT garment
             FROM garments G, garments_in_pattern A
             WHERE A.garment_id = G.id AND A.pattern_id=:pattern_id"""
    return db.session.execute(sql, {"pattern_id":pattern_id}).fetchall()

def get_garment_types():
    sql = "SELECT garment, id FROM garments ORDER BY id"
    return db.session.execute(sql).fetchall()

def count_companies():
    sql = "SELECT COUNT(DISTINCT company) FROM patterns"
    return db.session.execute(sql).fetchone()[0]
