from initialization import cnx, cur
from flask import render_template, url_for, redirect, request, session, Blueprint
from base64 import b64encode
from content_display_functions import showcasecontent
from common_functions import get_point, detectusername, add_to_cart, add_to_wishlist1

main = Blueprint('main', __name__)


def search_user(name):
    try:
        sql = '''SELECT user_.name_ as name_, user_.id as id FROM user_ WHERE user_.name_ like %s '''
        name = "%"+name+"%"
        values = [name]
        cur.execute(sql, values)
        users = cur.fetchall()
        ids = []
        for t in users:
            ids.append(t['id'])

        points=[]

        for id in ids:
            sql = ''' select if(order_.seller_id = %s, avg(order_.point_), NULL) as point_ from order_ where seller_id = %s'''
            values = [id, id]
            cur.execute(sql, values)
            x = cur.fetchone()
            points.append( x['point_'])

        for i in range (0,len(points)):
            if points[i] is None:
                users[i]['point_'] = "this user has no seller points yet"
            else:
                users[i]['point_'] = points[i]


        return users
    except Exception as e:
        return (0, e)


def search_user_vote_filter(name, min_vote, max_vote):
    try:
        sql = ''
        values = []

        if min_vote != '' and max_vote != '':
            sql = '''select user_.id as id, user_.name_ as name_, avg(order_.point_) as point_ from user_ inner join order_ on user_.id = order_.seller_id where user_.name_ like %s group by user_.id avg(order_.point_) > %s and avg(order_.point_) < %s'''
            name = "%"+name+"%"
            values = [name, float(min_vote), float(max_vote)]
        elif min_vote != '':
            sql = '''select user_.id as id, user_.name_ as name_, avg(order_.point_) as point_ from user_ inner join order_ on user_.id = order_.seller_id where user_.name_ like %s group by user_.id having avg(order_.point_) > %s'''
            name = "%"+name+"%"
            values = [name, float(min_vote)]
        elif max_vote != '':
            sql = '''select user_.id as id ,  user_.name_ as name_, avg(order_.point_) as point_ from user_ inner join order_ on user_.id = order_.seller_id where user_.name_ like %s group by user_.id having avg(order_.point_) < %s '''
            name = "%"+name+"%"
            values = [name,  float(max_vote)]

        cur.execute(sql, values)
        users = cur.fetchall()
        return users
    except Exception as e:
        return (0, e)


def search_book(name):
    try:
        sql = '''select user_.name_ as seller, user_.id as seller_id, M.name_ as title,M.book_id, book.book_image as book_image, book.number_of_pages as number_of_pages, book.condition_ as condition_, author.name_ as author, publisher.name_ as publisher, price.price as price from (user_ inner join (select book.name_, T.user_id, T.book_id from book inner join (select user_id, book_id from showcase where book_id in (select id from book where name_ like %s)) as T on T.book_id = book.id) as M on M.user_id = user_.id), book, author, publisher, price where book.id = M.book_id and author.id = book.author_id and publisher.id = book.publisher_id and (price.date_ = (select max(price.date_) from price where price.book_id=book.id group by price.book_id)) and book.display = %s;'''
        name = "%"+name+"%"
        values = [name,  True]
        cur.execute(sql, values)
        books = cur.fetchall()
        for book in books:
            # print(book)
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


def search_book_condition_filter(name, condition):
    try:
        sql = '''select user_.name_ as seller, user_.id as seller_id, M.name_ as title,M.book_id, book.book_image as book_image, book.number_of_pages as number_of_pages,book.condition_ as condition_, author.name_ as author, publisher.name_ as publisher, price.price as price from (user_ inner join (select book.name_, T.user_id, T.book_id from book inner join (select user_id, book_id from showcase where book_id in (select id from book where name_ like %s)) as T on T.book_id = book.id) as M on M.user_id = user_.id), book, author, publisher, price where book.id = M.book_id and author.id = book.author_id and publisher.id = book.publisher_id and (price.date_ = (select max(price.date_) from price where price.book_id=book.id group by price.book_id)) and book.display = %s and book.condition_ = %s;'''
        name = "%"+name+"%"
        values = [name, True, condition]
        cur.execute(sql, values)
        books = cur.fetchall()
        for book in books:
            if isinstance((book['book_image']), bytes):
                book['book_image'] = b64encode(
                    book['book_image']).decode("utf-8")
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


@main.route("/mainpage", methods=['GET', 'POST'])
def mainpage():
    name = session['username']
    if request.method == 'POST':
        if request.form['search_btn'] == 'user_search_btn':
            username_searched = request.form['search_user']
            return redirect(url_for('.user_searchresults', user_searched=username_searched))

        if request.form['search_btn'] == 'book_search_btn':
            book_searched = request.form['search_book']
            return redirect(url_for('.book_searchresults', book_searched=book_searched))

    return render_template('mainpage.html', name=name)


@main.route("/user_searchresults/<user_searched>", methods=['GET', 'POST'])
def user_searchresults(user_searched):
    users = search_user(user_searched)
    message = ''
    if request.method == "POST":
        min_vote = request.form['min_vote_value']
        max_vote = request.form['max_vote_value']
        if max_vote != '' and min_vote != '' and int(max_vote) < int(min_vote):
            message = "maximum vote cannot be smaller than minimum vote"
            return render_template('usersearchresults.html', len=len(users), user_searched=user_searched, users=users, message=message)

        users = search_user_vote_filter(user_searched, min_vote, max_vote)
        print(users)
        print("**")
        message = "search is successful"
        return render_template('usersearchresults.html', len=len(users), user_searched=user_searched, users=users, message=message)
    return render_template('usersearchresults.html', len=len(users), user_searched=user_searched, users=users)


@main.route("/book_searchresults/<book_searched>", methods=['GET', 'POST'])
def book_searchresults(book_searched):
    books = search_book(book_searched)
    message = ''

    if request.method == 'POST':
        condition = int(request.form['condition'])
        if condition != 0:
            books = search_book_condition_filter(book_searched, condition)
            return render_template('booksearchresult.html', len=len(books), books=books, book_searched=book_searched, message=message)
        try:
            if request.form['shop_btn'][:11] == "add_to_cart":
                book_id = request.form['shop_btn'][12:]
                message = add_to_cart(book_id)
            elif request.form['shop_btn'][:15] == "add_to_wishlist":
                book_id = request.form['shop_btn'][16:]
                message = add_to_wishlist1(book_id)
        except Exception as e:
            print(e)
    return render_template('booksearchresult.html', len=len(books), books=books, book_searched=book_searched, message=message)


@main.route("/anotheruser/<user_id>", methods=['GET', 'POST'])
def anotheruserpage(user_id):
    user_name = detectusername(user_id)
    books = showcasecontent(user_id)
    point = get_point(user_id)

    message = ''

    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        if request.form['shop_btn'] == "add_to_cart":
            message = add_to_cart(book_id)
        elif request.form['shop_btn'] == "add_to_wishlist":
            message = add_to_wishlist1(book_id)

    return render_template('anotheruserpage.html', len=len(books), user_name=user_name, books=books, message=message, point=point)
