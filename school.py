from initialization import cnx, cur
from flask import  render_template, url_for, redirect, request, session, Blueprint, flash
from base64 import b64encode
from common_functions import  add_to_cart, add_to_wishlist1


school = Blueprint('school', __name__)

def string_to_list(str):
    str = str[1: len(str)-1]
    temp = list(str.split(","))
    ints = []
    for i in temp:
        ints.append(int(i))

    return ints

def check_if_university_exists(university_searched):
    try:
        sql= '''select id from courses where university like %s '''
        university_searched = "%"+university_searched+"%"
        values=[university_searched]
        cur.execute(sql, values)
        course_ids = cur.fetchall()
        ids = []
        for id in course_ids:
            ids.append(id['id'])

        return ids

    except Exception as e:
        return False

def search_book(course_ids):
    try:
        books = []
        for id in course_ids:
            sql = '''select courses.university, courses.name_ as course, courses.professor, courses.term, user_.name_ as seller, user_.id as seller_id, M.name_ as title,M.book_id , book.book_image as book_image, book.condition_ as condition_, author.name_ as author, publisher.name_ as publisher, price.price as price from (user_ inner join (select book.name_, book.courses_id, T.user_id, T.book_id from book inner join (select user_id, book_id from showcase where book_id in (select id from book where courses_id = %s)) as T on T.book_id = book.id) as M on M.user_id = user_.id) inner join courses on courses.id = M.courses_id, book, author, publisher, price where book.id = M.book_id and author.id = book.author_id and publisher.id = book.publisher_id and (price.date_ = (select max(price.date_) from price where price.book_id=book.id group by price.book_id)) and book.display = %s;  '''
            values = [id, True]
            cur.execute(sql, values)
            temp = cur.fetchall()
            for t in temp:
                books.append(t)

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
        return (0, e)

def search_book_filtered(course_ids, course):
    try:
        books=[]
        for id in course_ids:
            sql = ''' select courses.university, courses.name_ as course, courses.professor, courses.term, user_.name_ as seller, user_.id as seller_id, M.name_ as title,M.book_id , book.book_image as book_image, book.condition_ as condition_, author.name_ as author, publisher.name_ as publisher, price.price as price from (user_ inner join (select book.name_, book.courses_id, T.user_id, T.book_id from book inner join (select user_id, book_id from showcase where book_id in (select id from book where courses_id in (select id from courses where id=%s and name_ like %s))) as T on T.book_id = book.id) as M on M.user_id = user_.id) inner join courses on courses.id = M.courses_id, book, author, publisher, price where book.id = M.book_id and author.id = book.author_id and publisher.id = book.publisher_id and (price.date_ = (select max(price.date_) from price where price.book_id=book.id group by price.book_id)) and book.display = %s;'''
            course = "%"+course+"%"
            values=[id, course, True]
            cur.execute(sql, values)
            temp = cur.fetchall()
            for t in temp:
                books.append(t)

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

@school.route('/schoolmode', methods= ['GET', 'POST'])
def schoolmode():
    if request.method == 'POST':
        if request.form['search_btn'] == "university_search_btn":
            university_searched = request.form['search_university']
            course_ids = check_if_university_exists(university_searched)

            if len(course_ids) != 0:
                return redirect(url_for('.course_search', course_ids = course_ids))

            flash('University not found')
            return redirect(url_for('.schoolmode'))

    return render_template('schoolmode.html')

@school.route('/course_search/<course_ids>', methods = ['GET', 'POST'])
def course_search(course_ids):
    course_ids = string_to_list(course_ids)
    books = search_book(course_ids)
    message = ''

    if request.method == 'POST':
        search_course = request.form['course_search']

        if search_course != '':
            books = search_book_filtered(course_ids, search_course)
            return render_template('schoolmode_coursesearch.html', len=len(books), books=books, message=message)
        try:
            if request.form['shop_btn'][:11] == "add_to_cart":
                book_id = request.form['shop_btn'][12:]
                message = add_to_cart(book_id)
            elif request.form['shop_btn'][:15] == "add_to_wishlist":
                book_id = request.form['shop_btn'][16:]
                message = add_to_wishlist1(book_id)
        except Exception as e:
            print(e)
    return render_template('schoolmode_coursesearch.html', len=len(books), books=books, message=message)