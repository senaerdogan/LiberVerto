from base64 import b64encode
from flask import session
from initialization import cnx, cur

def basketcontent():
    try:
        books = []
        sql = '''select book.book_image as book_image, book.name_ as title, book.id as id, author.name_ as author, publisher.name_ as publisher, book.condition_ as condition_, book.number_of_pages as number_of_pages, price as price, user_.name_ as seller, user_.id as seller_id  from book, author, publisher, price, user_ where ((user_.id in (select user_id from showcase where book_id = book.id)) and book.id in (select basket.book_id  from basket where basket.user_id = %s and basket.is_active = %s) and (book.author_id = author.id) and (book.publisher_id = publisher.id)  and (price.date_ = (select max(price.date_) from price where price.book_id=book.id group by price.book_id)) ); '''
        values = [int(session['id']), True]
        cur.execute(sql, values)
        books = cur.fetchall()
        for book in books:
            if isinstance((book['book_image']) , bytes):
                book['book_image'] = b64encode(book['book_image']).decode("utf-8")
            if book['condition_'] == 1:
                book['condition_'] = "Looks like new"
            elif book['condition_'] == 2:
                book['condition_'] = "Pre-owned but no writing"
            elif book['condition_'] == 3:
                book['condition_'] = "Only name written on cover"
            elif book['condition_'] == 4:
                book['condition_'] = "Highlighted and more"
        return books
    except Exception as e:
        return (0,e)

def wishlist1content():
    try:
        sql = '''select book.book_image as book_image, book.name_ as title, book.id as book_id, author.name_ as author, publisher.name_ as publisher,book.condition_ as condition_, book.number_of_pages as number_of_pages, price as price  from book, author, publisher, price where (book.id in (select wishlist_1.book_id  from wishlist_1 where wishlist_1.user_id = %s) and (book.author_id = author.id) and (book.publisher_id = publisher.id)  and (price.date_ = (select max(price.date_) from price where price.book_id=book.id group by price.book_id))); '''
        values = [int(session['id'])]
        cur.execute(sql, values)
        books = cur.fetchall()
        for book in books:
            if isinstance((book['book_image']) , bytes):
                book['book_image'] = b64encode(book['book_image']).decode("utf-8")
            if book['condition_'] == 1:
                book['condition_'] = "Looks like new"
            elif book['condition_'] == 2:
                book['condition_'] = "Pre-owned but no writing"
            elif book['condition_'] == 3:
                book['condition_'] = "Only name written on cover"
            elif book['condition_'] == 4:
                book['condition_'] = "Highlighted and more"
        return books
    except Exception as e:
        return (0,e)

def wishlist2content():
    try:
        sql = '''select book_name as title, author_name as author  from wishlist_2 where (wishlist_2.user_id = %s); '''
        values = [int(session['id'])]
        cur.execute(sql, values)
        books = cur.fetchall()
        return books
    except Exception as e:
        return (0,e)

def showcasecontent(user_id):
    try:
        if user_id == session['id']:
            sql = '''select book.book_image as book_image, book.name_ as title, book.id as id, author.name_ as author, publisher.name_ as publisher  from book, author, publisher where (book.id in (select showcase.book_id  from showcase where showcase.user_id = %s) and (book.author_id = author.id) and (book.publisher_id = publisher.id)); '''
            values = [int(user_id)]
        else: 
            sql = '''select book.book_image as book_image, book.name_ as title, book.id as id, author.name_ as author, publisher.name_ as publisher  from book, author, publisher where (book.id in (select showcase.book_id  from showcase where showcase.user_id = %s) and (book.author_id = author.id) and (book.publisher_id = publisher.id) and book.display = %s); '''
            values = [int(user_id), True]
        cur.execute(sql, values)
        books = cur.fetchall()
        for book in books:
            if isinstance((book['book_image']) , bytes):
                book['book_image'] = b64encode(book['book_image']).decode("utf-8")
        return books
    except Exception as e:
        print(e)
        return (0,e)
