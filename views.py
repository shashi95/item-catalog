from sqlalchemy import create_engine, desc
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, SportCatagory, Item
from flask import session as login_session
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from datetime import datetime
import random
import string
from flask import make_response
import requests

engine = create_engine('sqlite:///sports.db',connect_args={'check_same_thread': False});
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

#main page
@app.route('/')
@app.route('/catalogs')
def showCatalog():
	"""Show catalogs"""
	sports = session.query(SportCatagory).all()
	items = session.query(Item).order_by(desc(Item.time_updated)).limit(6)
	for item in items:
		print(item.name, item.time_updated)
	if 'username' not in login_session:
		return render_template('publicsports.html', sports=sports, items = items)
	else:
		return render_template('sports.html', sports=sports, items = items)



@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    print(login_session['state'])
    print(request.args.get('state'))
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

#Show items for given sport catagory
@app.route('/catalog/<string:sport_name>/items/')
def showItem(sport_name):
	sports = session.query(SportCatagory).all()
	items = session.query(Item).filter_by(sport_name=sport_name).all()
	if 'username' not in login_session:
		return render_template('publicitems.html', items=items, sports=sports, selected_sport = sport_name)
	else:
		return render_template('item.html', items=items, sports=sports, selected_sport = sport_name)


#Show item description for given item
@app.route('/catalog/<string:sport_name>/<string:item_name>')
def showItemDescription(sport_name, item_name):
	item = session.query(Item).filter_by(name=item_name).filter_by(sport_name=sport_name).one()
	if 'username' not in login_session:
		return render_template('publicitemdescription.html', item=item)
	else:
		return render_template('itemdescription.html', item=item)

#add new item 
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
		sport_name = str(request.form.get('category'))
		sport  = session.query(SportCatagory).filter_by(name=sport_name).one()
		item_name = request.form['name']
		if item_name == '':
			flash("Item name can not be empty!!")
			return redirect(url_for('showCatalog'))
		result = session.query(Item).filter_by(sport_name=sport_name).filter_by(name=item_name).first()
		if result == None:
			newItem = Item(name = item_name, description=request.form['description'], time_updated = datetime.now(), sport=sport)
			session.add(newItem)
			session.commit()
			flash('New Item %s Item Successfully Created' % (newItem.name))
		else:
			flash("Item with same name already exists in this sport catagory")
 		return redirect(url_for('showCatalog'))
    else:
        return render_template('newitem.html')


#Edit item
@app.route('/catalog/<string:sport_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(sport_name, item_name):
    editedItem = session.query(Item).filter_by(name=item_name).filter_by(sport_name=sport_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form.get('category'):
            editedItem.sport_name = request.form.get('category')
        session.add(editedItem)
       	session.commit()
        flash('Item Successfully Edited %s' % editedItem.name)
        return redirect(url_for('showCatalog'))
    else:
        return render_template('edititems.html', item=editedItem)


@app.route('/catalog/<string:sport_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(sport_name, item_name):
    itemToDelete = session.query(Item).filter_by(name=item_name).filter_by(sport_name=sport_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteitem.html', item=itemToDelete)



@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))



@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalogs/JSON')
def catalogsJSON():
	sports = session.query(SportCatagory).all()
	items = session.query(Item).all()
	result = []
	for sport in sports:
		itemlist = [item for item in items if item.sport_name == sport.name]
		result.append(serialize(sport, itemlist))
	return jsonify(Category=result)


def serialize(sport, items):
	i = [{'id': item.id, 'title': item.name , 'description': item.description, 'cat_id': sport.id} for item in items]
	return {
		'id': sport.id,
		'name': sport.name,
		'Item': i
	}

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)