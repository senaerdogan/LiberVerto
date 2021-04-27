from initialization import cnx, cur
from flask import session

def get_point(user_id):
    try:
        # sql = '''select avg(star) from give_point where seller_id = %s '''
        sql = '''select avg(point_) from order_ where seller_id  = %s '''
        values = [int(user_id)]
        cur.execute(sql,values)
        point = cur.fetchone()
        point = point['avg(point_)']
        if point == None:
            return "no points yet"
        return point
    except Exception as e:
        return (0,e)

def detectusername(user_id):
    try:
        sql = '''select name_ from user_ where id = %s'''
        values = [int(user_id)]
        cur.execute(sql, values)
        user_name = cur.fetchall()
        return user_name[0]['name_']
    except Exception as e:
        return (0, e)

def give_point(point, basket_id):
    try:
        sql = '''select point_ from order_ where basket_id = %s '''
        values = [int(basket_id)]
        cur.execute(sql, values)
        points = cur.fetchone()
        if points['point_'] != None:
            return "Error: You have given point to this book already"
        
        sql = '''update order_ set point_ = %s where order_.basket_id = %s'''
        values = [int(point), int(basket_id)]
        cur.execute(sql, values)
        cnx.commit()
        return "You have given point successfully"

    except Exception as e:
        return (0,e)

def add_to_wishlist2(title, author):
    try:
        sql = '''insert into wishlist_2 (user_id, book_name, author_name) values (%s, %s, %s) '''
        values = [int(session['id']), title, author]
        cur.execute(sql, values)
        cnx.commit()
        return "successfuly added new book to wishlist 2"

    except Exception as e:
        return (0,e)

def add_to_cart(book_id):
    try:
        sql = '''(select user_id from showcase where book_id = %s) '''
        values =[int(book_id)]
        cur.execute(sql, values)
        seller_id = cur.fetchone()
        seller_id = seller_id['user_id']

        
        if seller_id != session['id']:
            sql = '''select basket.id from basket where book_id = %s and user_id = %s and is_active = %s'''
            values = [int(book_id), int(session['id']), True]
            cur.execute(sql,values)
            exists = cur.fetchall()
            if exists:
                return "This book has already added to your basket"

            sql = '''insert into basket (book_id, user_id) values (%s, %s) '''
            values = [int(book_id), int(session['id'])]
            cur.execute(sql, values)
            cnx.commit()
            return ("added to cart successfully")
        else: 
            return ("a user can not add his/her book into his/her basket")
    except Exception as e:
        return("exception occured")

#wishlist for already existing books 
def add_to_wishlist1(book_id):
    try:
        sql = '''select user_id from showcase where book_id = %s '''
        values = [book_id]
        cur.execute(sql, values)
        seller_id = cur.fetchone()
        seller_id = seller_id['user_id']
        if seller_id != session['id']:
            sql = '''insert into wishlist_1 (book_id, user_id) values (%s, %s) '''
            values = [int(book_id), int(session['id'])]
            cur.execute(sql, values)
            cnx.commit()
            return ("added to wishlist successfully")
        else: 
            return ("a user can not add his/her book into his/her wishlist")
    except Exception as e:
        print(e)
        return("exception occured")

def course_exists(university, professor, term, course):
    try:
        sql = '''select id from courses where university = %s and professor = %s and term = %s and name_ = %s '''
        values = [university, professor, term, course]
        cur.execute(sql, values)
        course_id = cur.fetchone()

        if course_id == None: #no such course exists before
            sql = '''insert into courses (name_, university, professor, term) values (%s, %s, %s, %s)'''
            values = [course, university, professor, term]
            cur.execute(sql, values)
            cnx.commit()
            sql = '''select last_insert_id()'''
            cur.execute(sql)
            course_id = cur.fetchone()
            course_id = course_id.get('last_insert_id()')

        return (1,course_id)   
    except Exception as e:
        return (0,e)


