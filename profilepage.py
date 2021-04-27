import traceback
from initialization import cnx, cur
from flask import  render_template, url_for, redirect, request, session, Blueprint
from content_display_functions import showcasecontent,  wishlist2content
from common_functions import get_point, add_to_wishlist2, course_exists

profile = Blueprint('profile', __name__)


def addbook(title, author, publisher, publish_year, number_of_pages, price, condition, onShowcase, book_image):
    try:
        sql = '''select id from author where name_ = %s '''
        values = [author]
        cur.execute(sql,values)
        author_id = cur.fetchone()
        
        if author_id == None: 
            #add new author to database
            sql = '''insert into author (name_) values (%s)'''
            values = [author]
            cur.execute(sql, values)
            cnx.commit()
            sql = '''select last_insert_id()'''
            cur.execute(sql)
            author_id = cur.fetchone()
            author_id = author_id.get('last_insert_id()')            
        else: 
            author_id = author_id.get('id')

        author_id = int(author_id)

        sql = '''select id from publisher where name_ = %s '''
        values = [publisher]
        cur.execute(sql,values)
        publisher_id = cur.fetchone()
        
        if publisher_id == None: 
            #add new publisher to database
            sql = '''insert into publisher (name_) values (%s)'''
            values = [publisher]
            cur.execute(sql, values)
            cnx.commit()
            sql = '''select last_insert_id()'''
            cur.execute(sql)
            publisher_id = cur.fetchone()
            publisher_id = publisher_id.get('last_insert_id()')
        else: 
            publisher_id = publisher_id.get('id')


        sql = '''insert into book (name_, author_id, publisher_id, publish_year, number_of_pages, condition_, display, book_image) values (%s, %s, %s, %s, %s, %s, %s, %s) '''
        values = [title, int(author_id), int(publisher_id), int(publish_year), int(number_of_pages),  int(condition), onShowcase, book_image]
        cur.execute(sql,values)
        cnx.commit()

        sql = '''select last_insert_id()'''
        cur.execute(sql)
        book_id = cur.fetchone()
        book_id = book_id.get('last_insert_id()')

        sql = ''' insert into price (price, book_id) values (%s,  %s)'''
        values= [float(price), int(book_id)]
        cur.execute(sql, values)
        cnx.commit()

        #add to user's showcase
        user_id = session['id']

        sql = ''' insert into showcase (book_id, user_id) values (%s, %s)'''
        values = [int(book_id) , int(user_id)]
        cur.execute(sql,values)
        cnx.commit()

    except Exception as e:
        return (0,e)
    
def addbook_schoolmode(title, author, publisher, publish_year, number_of_pages, price, condition, onShowcase, book_image, university, professor, term, course):
    try:
        sql = '''select id from author where name_ = %s '''
        values = [author]
        cur.execute(sql,values)
        author_id = cur.fetchone()
        
        if author_id == None: 
            #add new author to database
            sql = '''insert into author (name_) values (%s)'''
            values = [author]
            cur.execute(sql, values)
            cnx.commit()
            sql = '''select last_insert_id()'''
            cur.execute(sql)
            author_id = cur.fetchone()
            author_id = author_id.get('last_insert_id()')            
        else: 
            author_id = author_id.get('id')

        author_id = int(author_id)

        sql = '''select id from publisher where name_ = %s '''
        values = [publisher]
        cur.execute(sql,values)
        publisher_id = cur.fetchone()
        
        if publisher_id == None: 
            #add new publisher to database
            sql = '''insert into publisher (name_) values (%s)'''
            values = [publisher]
            cur.execute(sql, values)
            cnx.commit()
            sql = '''select last_insert_id()'''
            cur.execute(sql)
            publisher_id = cur.fetchone()
            publisher_id = publisher_id.get('last_insert_id()')
        else: 
            publisher_id = publisher_id.get('id')

        course_id = course_exists(university=university, professor=professor, term=term, course=course)
        if course_id[0] == 1:
            course_id = (course_id[1])
        else:
            return "an error occured"

       
        sql = '''insert into book (name_, author_id, publisher_id, publish_year, number_of_pages, condition_, display, book_image, courses_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) '''
        values = [title, int(author_id), int(publisher_id), int(publish_year), int(number_of_pages),  int(condition), onShowcase, book_image, int(course_id)]
        cur.execute(sql,values)
        cnx.commit()

        sql = '''select last_insert_id()'''
        cur.execute(sql)
        book_id = cur.fetchone()
        book_id = book_id.get('last_insert_id()')

        sql = ''' insert into price (price, book_id) values (%s,  %s)'''
        values= [float(price), int(book_id)]
        cur.execute(sql, values)
        cnx.commit()

        #add to user's showcase
        user_id = session['id']

        sql = ''' insert into showcase (book_id, user_id) values (%s, %s)'''
        values = [int(book_id) , int(user_id)]
        cur.execute(sql,values)
        cnx.commit()

    except Exception as e:
        traceback.print_exc()
        return (0,e)

def updatebook(book_id, title, author, publisher, publish_year, number_of_pages, price, condition, onShowcase, book_image):
    try:
        sql= '''select book.name_ as cur_title, author.name_ as cur_author, publisher.name_ as cur_publisher, price.price as cur_price, book.book_image as cur_book_image, book.number_of_pages as cur_number_of_pages, book.publish_year as cur_publish_year, book.condition_ as cur_condition, book.display as cur_onShowcase from book, author, publisher, price where (book.id = %s and author.id = book.author_id and publisher.id = book.publisher_id and price.book_id = %s) '''
        values=[int(book_id), int(book_id)]
        cur.execute(sql,values)
        cur_book = cur.fetchone()

        cur_condition = cur_book['cur_condition']
        cur_onShowcase = cur_book['cur_onShowcase']


        update_sql = "update book set "
        update_values = []
        update_temp = []


        if title != "":
            update_temp.append(" name_ = %s")
            update_values.append(title)

        if author != "":
            #check if author exists
            update_temp.append(" author_id = %s ")
            sql = '''select id from author where name_ = %s '''
            values = [author]
            cur.execute(sql,values)
            author_id = cur.fetchone()
            
            if author_id == None: 
                #add new author to database
                sql = '''insert into author (name_) values (%s)'''
                values = [author]
                cur.execute(sql, values)
                cnx.commit()
                sql = '''select last_insert_id()'''
                cur.execute(sql)
                author_id = cur.fetchone()
                author_id = author_id.get('last_insert_id()')            
            else: 
                author_id = author_id.get('id')

            update_values.append(int(author_id))

        if publisher != "":            
            update_temp.append(" publisher_id = %s ")
            #check if publisher exists
            sql = '''select id from publisher where name_ = %s '''
            values = [publisher]
            cur.execute(sql,values)
            publisher_id = cur.fetchone()
            
            if publisher_id == None: 
                #add new publisher to database
                sql = '''insert into publisher (name_) values (%s)'''
                values = [publisher]
                cur.execute(sql, values)
                cnx.commit()
                sql = '''select last_insert_id()'''
                cur.execute(sql)
                publisher_id = cur.fetchone()
                publisher_id = publisher_id.get('last_insert_id()')
            else: 
                publisher_id = publisher_id.get('id')
            update_values.append(int(publisher_id))

        if publish_year != "":
            update_temp.append(" publish_year = %s")
            update_values.append(int(publish_year))

        if number_of_pages != "":
            update_temp.append(" number_of_pages = %s")
            update_values.append(int(number_of_pages))
        
        if price != "":
            #insert price
            sql = ''' insert into price (price, book_id) values (%s,  %s)'''
            values_= [float(price), int(book_id)]
            cur.execute(sql, values_)
            cnx.commit()
        
        if (condition != cur_condition) and (condition != "0"):
            update_temp.append(" condition_ = %s")
            update_values.append(int(condition))
        
        if onShowcase != cur_onShowcase:
            update_temp.append(" display = %s")
            update_values.append(onShowcase)
        
        if book_image != b'':
            update_temp.append(" book_image = %s")
            update_values.append(book_image)

        update_values.append(int(book_id))
        update_sql += ",".join(update_temp)
        update_sql += " where id = %s"
        cur.execute(update_sql, update_values)
        
        cnx.commit()
        return cur_book
    except Exception as e:
        return (0,e)

def deletebook(book_id):
    try:
        sql= '''delete from book where id = %s '''
        values = [int(book_id)]
        cur.execute(sql,values)
        cnx.commit()
        return "book deleted successfully"
    except Exception as e:
        return (0,e)

def update_user(newname, newaddress, newpassword):
    try:
        update_sql = "update user_ set "
        update_values = []
        update_temp = []

        if newname != "":
            update_temp.append(" name_ = %s")
            update_values.append(newname)

        if newaddress != "":
            update_temp.append(" address = %s")
            update_values.append(newaddress)

        if newpassword != "":
            update_temp.append(" password_ = %s")
            update_values.append(newpassword)

        update_values.append(int(session['id']))
        update_sql += ",".join(update_temp)
        update_sql += " where id = %s"
        cur.execute(update_sql, update_values)
        cnx.commit()

        session['username'] = newname

    except Exception as e:
        return (0,e)

def delete_from_wishlist2(book_title, book_author):
    try:
        sql = '''delete from wishlist_2 where user_id = %s and book_name = %s and author_name = %s '''
        values = [int(session['id']), book_title, book_author]
        cur.execute(sql, values)
        cnx.commit()
        return "successfully deleted"

    except Exception as e:
        return (0,e)

def delete_account():
    try:
        sql = '''delete from user_ where id = %s '''
        values=[int(session['id'])]
        cur.execute(sql, values)
        cnx.commit()

    except Exception as e:
        return "error"
#on update display all properties of book's
@profile.route("/profilepage", methods=['GET', 'POST'])
def profilepage():
    name = session['username']
    booksOnShowcase = showcasecontent(session['id'])
    point = get_point(session['id'])
    if request.method == 'POST':
        if request.form['profile_page_btn'] == 'add_book_btn':     
            title = request.form['name']
            author = request.form['author']
            publisher = request.form['publisher']
            publish_year = request.form['publish_year']
            number_of_pages = request.form['number_of_pages']
            price = request.form['price']
            cond_number = request.form['condition']
            
            onShowcase = True
            try: 
                request.form['onShowcase']  #if this line works, that means checkbox is checked
            except Exception as e : 
                onShowcase = False     
            book_image=''
            if request.files:
                image = request.files["addimage"]
                book_image = image.read()
                
      
            addbook(title, author, publisher, publish_year, number_of_pages, price, cond_number, onShowcase, book_image)
            return redirect(url_for('.profilepage'))
        
        if request.form['profile_page_btn'] == 'add_book_schoolmode_btn':
            #first check if course already exists, if not add 
            university = request.form['university']
            professor = request.form['professor']
            term = request.form['term']
            course = request.form['course']

            title = request.form['name']
            author = request.form['author']
            publisher = request.form['publisher']
            publish_year = request.form['publish_year']
            number_of_pages = request.form['number_of_pages']
            price = request.form['price']
            cond_number = request.form['condition']
            
            onShowcase = True
            try: 
                request.form['onShowcase']  #if this line works, that means checkbox is checked
            except Exception as e : 
                onShowcase = False     
            book_image=''
            if request.files:
                image = request.files["addimage"]
                book_image = image.read()
      
            addbook_schoolmode(title, author, publisher, publish_year, number_of_pages, price, cond_number, onShowcase, book_image, university, professor, term, course)
            return redirect(url_for('.profilepage'))
        
        if request.form['profile_page_btn'] == 'update_book_btn':
            title = request.form['name']
            author = request.form['author']
            publisher = request.form['publisher']
            publish_year = request.form['publish_year']
            number_of_pages = request.form['number_of_pages']
            price = request.form['price']
            cond_number = request.form['condition']
            
            onShowcase = True
            try: 
                request.form['onShowcase']  #if this line works, that means checkbox is checked
            except Exception as e : 
                onShowcase = False     
            book_image=''
            if request.files:
                image = request.files["updateimage"]
                book_image = image.read()

            temp = request.form['book_id']
            book_id = temp[7:]
            updatebook(book_id, title, author, publisher, publish_year, number_of_pages, price, cond_number, onShowcase, book_image) 
            return redirect(url_for('.profilepage'))
        if request.form['profile_page_btn'] == 'delete_book_btn':
            temp = request.form['book_id_delete']
            book_id = temp[7:]
            deletebook(book_id)
            return redirect(url_for('.profilepage'))
        
        if request.form['profile_page_btn'] == "update_user_info_btn":
            new_name = request.form['newname']
            new_address = request.form['newaddress']
            new_password = request.form['newpassword']
            update_user(newaddress=new_address, newname=new_name, newpassword=new_password)
            return redirect(url_for('.profilepage'))

        if request.form['profile_page_btn'] == 'delete_account_btn':
            delete_account()
            return redirect(url_for('landing.landingpage'))

        

    elif request.method == 'GET':
        booksOnShowcase = showcasecontent(session['id'])

    return render_template('profilepage.html', name=name, books= booksOnShowcase, point=point)


@profile.route("/wishlist2", methods=['GET', 'POST'])
def wishlist2():
    message = ''
    if request.method == 'POST':
        if request.form['wishlist2_page_btn'] == 'add_book_btn':
            title = request.form['name']
            author = request.form['author']
            add_to_wishlist2(title, author)
        elif request.form['wishlist2_page_btn'] == 'delete_book_btn':
            #in wishlist 2, there was no id, title, user_id and author together can sepesify a record, however
            temp = request.form['book_id_delete']
            temp = temp.split("_")
            book_title = temp[1]
            book_author = temp[2]
            message = delete_from_wishlist2(book_title, book_author)
    books = wishlist2content()   
    return render_template('wishlist2.html', books = books, message=message)






