#for wishlist 1 & basket & order & past orders
from initialization import cnx, cur
from flask import  render_template, url_for, redirect, request, session, Blueprint, flash
from base64 import b64encode
from content_display_functions import  basketcontent, wishlist1content
from common_functions import  give_point

shop = Blueprint('shop', __name__)

#MAY NEED TO USE TRANSACTIONS HERE, LOOK IT UP
def transfer_from_wishlist1_to_basket(book_ids):
    try:
        #delete these books from wishlist 1
        for id in book_ids:
            sql = '''delete from wishlist_1 where user_id = %s and book_id = %s '''
            values =[int(session['id']), int(id)]
            cur.execute(sql,values)
            cnx.commit()

        #add these books to basket
        for id in book_ids:
            sql = ''' insert into basket ( book_id, user_id ) values (%s, %s) '''
            values =[int(id), int(session['id'])]
            cur.execute(sql, values)
            cnx.commit()

        return "succesfull"

    except Exception as e:
        return (0,e)

def retrieve_past_orders():
    try:
        dates = []
        sql = ''' select date_ from order_ where user_id = %s group by user_id,date_,total_cost order by date_ desc'''
        values=[int(session['id'])]
        cur.execute(sql,values)
        dates = cur.fetchall()
 # 
        #keys are dates, values are books
        past_order_info = {}
        for date in dates:
            sql= '''select author.name_ as author, book.name_ as title, publisher.name_ as publisher, T.seller_id, user_.name_ as seller, T.basket_id, book.book_image as book_image, T.user_id, T.date_ , price.price as price, book.number_of_pages as number_of_pages, book.condition_ as condition_, book.publish_year as publish_year from book inner join (select basket_id, book_id, seller_id, order_.user_id, order_.date_ from order_ inner join basket on order_.basket_id = basket.id) as T on book.id = T.book_id, author, publisher, user_, price where author.id = book.author_id and publisher.id = book.publisher_id and user_.id = T.seller_id and (price.date_ = (select max(price.date_) from price where price.book_id=book.id group by price.book_id) ) and T.user_id = %s and T.date_ = %s'''
            date_ = date['date_']
            values =[int(session['id']),date_]
            # print(session['id'])
            cur.execute(sql,values)
            books = cur.fetchall()
            # print(books)
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
            past_order_info[date['date_']] = books


        return past_order_info

    except Exception as e:
        return (0,e)

#MAY NEED TO USE TRANSACTIONS HERE, LOOK IT UP
def place_order(address,payment_type, total_cost):
    try:
        #first retrieve basket id's by selecting rows with is_active = true
        sql= ''' select basket.id, basket.book_id, user_.id as seller_id, price.id as price_id from basket, user_, price where (user_id = %s and is_active = %s) and (user_.id in (select user_id from showcase where showcase.book_id = basket.book_id)) and (price.date_ = (select max(price.date_) from price where price.book_id=basket.book_id group by price.book_id)) '''
        values = [int(session['id']), True]
        cur.execute(sql, values)
        basket_ids = cur.fetchall()

        #add new record to order_ table
        for basket in basket_ids:
            sql = '''insert into order_  (user_id, address, payment_type, total_cost, basket_id, seller_id, price_id)  values (%s, %s, %s, %s, %s, %s, %s)''' 
            values = [int(session['id']), address, payment_type, float(total_cost), int(basket['id']), int(basket['seller_id']), int(basket['price_id'])]
            cur.execute(sql, values)
            cnx.commit()

        
        for basket in basket_ids:
            #transfer books to new owner
            sql = '''update showcase set user_id = %s where book_id = %s '''
            values = [int(session['id']), basket['book_id']]
            cur.execute(sql, values)
            cnx.commit()
            
            #DO THIS FIRST
            #delete from own wishlist_1
            #if that book is purchased directly from basket, may still present at wishlist, remove it
            sql = '''delete from wishlist_1 where user_id = %s and book_id = %s '''
            values = [int(session['id']), basket['book_id']]
            cur.execute(sql, values)
            cnx.commit() 

            #update wishlist_1 
            sql = '''update wishlist_1 set user_id = %s where book_id = %s '''
            values = [int(session['id']), basket['book_id']]
            cur.execute(sql, values)
            cnx.commit()

            #deactivate old baskets
            sql = '''update basket set is_active = %s where user_id = %s or book_id = %s'''
            values = [False, session['id'], basket['book_id']]
            cur.execute(sql, values)
            cnx.commit()


    except Exception as e:
        return (0,e)

def delete_from_wishlist1(book_id):
    try:
        sql = ''' delete from wishlist_1 where user_id = %s and book_id = %s'''
        values =[int(session['id']), book_id]
        cur.execute(sql, values)
        cnx.commit()
        return "successfully deleted"
    except Exception as e:
        return (0,e)

def delete_from_basket(book_id):
    try:
        sql = ''' delete from basket where user_id = %s and book_id = %s'''
        values =[int(session['id']), book_id]
        cur.execute(sql, values)
        cnx.commit()

        return "successfully deleted"
    except Exception as e:
        return (0,e)

#NOT OPERATIONAL, JUST FOR GRADE PURPOSES
def delete_from_order():
    try:
        sql = '''delete from order_ where user_id = %s '''
        values = [int(session['id'])]
        cur.execute(sql, values)
        cnx.commit()

    except Exception as e:
        return "error"

@shop.route("/basket" , methods=['GET', 'POST'])
def basket():
    books = basketcontent() 
    total_cost = 0
    for book in books:
        total_cost += book['price']
    if request.method == "POST":
        if request.form['basket_page_btn'] == 'place_order_btn':
            address= request.form['address']
            payment_type = request.form['payment_type']
            place_order(address, payment_type, total_cost)
        elif request.form['basket_page_btn'] == 'delete_book_btn':
            book_id = request.form['book_id_delete']
            book_id = int(book_id[7:])
            message=delete_from_basket(book_id)
            flash(message)

        return redirect(url_for('.basket'))
    

    return render_template('basket.html', books = books, total_cost = total_cost)


@shop.route("/wishlist1", methods= ['GET', 'POST'])
def wishlist1():
    books = wishlist1content() 
    message = '' 
    if request.method == "POST":
        if request.form['wishlist1_btn'] == "add_to_basket":
            selected_books = request.form.getlist("checkboxes")
            
            if len(selected_books) == 0:
                flash("You did not choose any book")
                return redirect(url_for('.wishlist1'))

            transfer_from_wishlist1_to_basket(selected_books)
            return redirect(url_for('.basket'))
        elif request.form['wishlist1_btn'] == 'delete_book_btn':
            book_id = request.form['book_id_delete']
            book_id = int(book_id[7:])
            message = delete_from_wishlist1(book_id)
            flash(message)
            return redirect(url_for('.wishlist1'))

    return render_template('wishlist1.html', books = books, message=message)


@shop.route("/past_orders", methods=['GET', 'POST'])
def past_orders():
    past_orders = retrieve_past_orders()
    message = ''
    if request.method == "POST":
        point = request.form['point']
        give_point_basket_id = (request.form['give_point_basket_id'])[10:]
        give_point_seller_id = (request.form['give_point_seller_id'])[10:]
        message = give_point(basket_id= give_point_basket_id, point=point)
        return render_template('pastorders.html', past_orders=past_orders, message = message)

    
    return render_template('pastorders.html', past_orders=past_orders )