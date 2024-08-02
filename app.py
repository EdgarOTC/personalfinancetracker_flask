# from flask import Flask, render_template, request, redirect, url_for
# import requests
import datetime
import models as M
import functions as F
import pandas as P
import matplotlib.pyplot as MP
# view functions ( in the MVT pattern)
# Route to the home page
@M.app.route('/')
def home():
    return M.render_template('index.html')

@M.app.route('/home', methods=['GET', 'POST'])
def index():
    return M.render_template('index.html')

@M.app.route('/persons', methods=['GET', 'POST'])
def persons():
    persons = M.Persons.query.all()
    return M.render_template('persons.html', persons=persons)

@M.app.route('/new_person', methods=['GET', 'POST'])
def new_person():
    if M.request.method == 'POST':
        name = M.request.form['name']
        new_person = M.Persons(name=name)
        M.db.session.add(new_person)
        M.db.session.commit()
        print("this is my updated database", new_person)
        return M.redirect(M.url_for('persons'))

    return M.render_template('new_person.html')

@M.app.route('/update_person/<id>', methods=['GET', 'POST'])
def update_person(id):
    person = M.db.session.execute(M.db.select(M.Persons).filter_by(id=id)).scalar_one()  
    if M.request.method == 'POST':
        name = M.request.form['name']
        person.name = name
        M.db.session.commit()
        return M.redirect(M.url_for('persons'))

    return M.render_template('update_person.html', person=person)

@M.app.route('/delete_person/<id>', methods=['GET', 'POST'])
def delete_person(id):
    person = M.db.session.execute(M.db.select(M.Persons).filter_by(id=id)).scalar_one()
    if M.request.method == 'POST':
        M.db.session.delete(person)
        M.db.session.commit()
        return M.redirect(M.url_for('persons'))
    
    return M.render_template('delete_person.html', person=person)

@M.app.route('/categories', methods=['GET', 'POST'])
def categories():    
    categories = M.Categories.query.all()
    return M.render_template('categories.html', categories=categories)

@M.app.route('/new_category', methods=['GET', 'POST'])
def new_category():
    if M.request.method == 'POST':
        name = M.request.form['name']
        type = M.request.form['type']
        new_category = M.Categories(name=name,type=type)
        M.db.session.add(new_category)
        M.db.session.commit()        
        return M.redirect(M.url_for('categories'))
    
    return M.render_template('new_category.html')

@M.app.route('/update_category/<id>', methods=['GET', 'POST'])
def update_category(id):
    category = M.db.session.execute(M.db.select(M.Categories).filter_by(id=id)).scalar_one()     
    if M.request.method == 'POST':
        name = M.request.form['name']
        category.name = name
        M.db.session.commit()
        return M.redirect(M.url_for('categories'))

    return M.render_template('update_category.html', category=category)

@M.app.route('/delete_category/<id>', methods=['GET', 'POST'])
def delete_category(id):
    category = M.db.session.execute(M.db.select(M.Categories).filter_by(id=id)).scalar_one()
    if M.request.method == 'POST':
        M.db.session.delete(category)
        M.db.session.commit()
        return M.redirect(M.url_for('categories'))
    
    return M.render_template('delete_category.html', category=category)

@M.app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    categories = M.Categories.query.all()
    persons = M.Persons.query.all()            
    transactions = M.Transactions.query.all()
    return M.render_template('transactions.html', transactions=transactions, categories=categories, persons=persons)

@M.app.route('/new_transaction', methods=['GET', 'POST'])
def new_transaction():
    categories = M.Categories.query.all()
    persons = M.Persons.query.all()    
    if M.request.method == 'POST':
        description = M.request.form['description']
        date = str(M.request.form['date'])
        date = date.split('-')
        date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
        amount = M.request.form['amount']
        category = str(M.request.form['category'])
        category = category.replace(' ','')
        if category == '':
            message = "Transaction could not be created because category field is missing"
            return M.render_template('error.html', message=message)            
        category = category.split('-')
        if len(category) <= 1 or category[0].isdigit == False :
            message = "Category field is not from the expected type"
            return M.render_template('error.html', message=message)                   
        category = int(category[0])
        cat_res = F.get_element(categories,category)
        if len(list(filter(lambda x: x.id == category, categories))) == 0:
            message = f"Transaction could not be created because category field provided does not exist. type(cat_res): {type(cat_res)}"
            return M.render_template('error.html', message=message)

        person = str(M.request.form['person'])
        person = person.replace(' ','')
        if person == '':
            message = "Transaction could not be created because person field is missing"
            return M.render_template('error.html', message=message)
        person = person.split('-')
        if len(person) <= 1 or person[0].isdigit == False:
            message = "Person field is not from the expected type"
            return M.render_template('error.html', message=message)        
        person = int(person[0])
        # if F.get_element(persons,category) not in persons:
        if len(list(filter(lambda x: x.id == person, persons))) == 0:        
            message = "Transaction could not be created because person field provided does not exist"
            return M.render_template('error.html', message=message)
        new_transaction = M.Transactions(description=description,date=date,amount=amount,category=category,person=person)
        M.db.session.add(new_transaction)
        M.db.session.commit()        

        return M.redirect(M.url_for('transactions'))
    
    return M.render_template('new_transaction.html', categories=categories, persons=persons)

@M.app.route('/update_transaction/<id>', methods=['GET', 'POST'])
def update_transaction(id):
    transaction = M.db.session.execute(M.db.select(M.Transactions).filter_by(id=id)).scalar_one() 
    categories = M.Categories.query.all()
    persons = M.Persons.query.all()       
    if M.request.method == 'POST':
        transaction.description = M.request.form['description']
        date = M.request.form['date'].split('-')
        date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
        transaction.date = date
        transaction.amount = M.request.form['amount']
        category = M.request.form['category']
        person = M.request.form['person']
        transaction.category = category.split('-')[0]
        transaction.person = person.split('-')[0]
        M.db.session.commit()
        return M.redirect(M.url_for('transactions'))

    return M.render_template('update_transaction.html', transaction=transaction, categories=categories, persons=persons)

@M.app.route('/delete_transaction/<id>', methods=['GET', 'POST'])
def delete_transaction(id):
    transaction = M.db.session.execute(M.db.select(M.Transactions).filter_by(id=id)).scalar_one()
    categories = M.Categories.query.all()
    persons = M.Persons.query.all()             
    if M.request.method == 'POST':
        M.db.session.delete(transaction)
        M.db.session.commit()
        return M.redirect(M.url_for('transactions'))
    
    return M.render_template('delete_transaction.html', transaction=transaction, categories=categories, persons=persons)

@M.app.route('/reports', methods=['GET', 'POST'])
def reports():
    return M.render_template('reports.html')

@M.app.route('/transactions_rpt', methods=['GET', 'POST'])
def transactions_rpt():
    categories = M.Categories.query.all()
    # categories = M.db.session.execute(M.db.select(M.Categories).order_by(M.Categories.id)).scalars()
    persons = M.Persons.query.all()            
    transactions = M.Transactions.query.all()
    trans_ds = {
        # "Categories":list(categories),
        # "Persons":list(persons),
        "Transactions":F.TransData_Dict(transactions)
        # "Transactions":transactions
        }
    
    # ds = P.DataFrame(trans_ds)
    ds = P.DataFrame(F.TransData_Dict(transactions))
    # ds = P.Series(trans_ds, index = [1,2])
    # ds = P.DataFrame(trans_ds)
    print(ds)
    # ds = type(categories)
    return M.render_template('transactions_rpt.html', ds=ds)

if __name__ == '__main__':
    
    # create the database
    with M.app.app_context():
        M.db.create_all()
    M.app.run(debug=True)