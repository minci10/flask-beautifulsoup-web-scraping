from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup, SoupStrainer
import lxml
from config import DB_URI


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(150), nullable=False)
    price = db.Column(db.String(10), nullable=False, default="0.00")

    def __repr__(self):
        return '<Task %r>' % self.id

db.create_all()

def scrape_data(url):
    r = requests.get(url)
    data = r.content
    strainer = SoupStrainer('div', attrs={'id': 'listing-right-column'})
    soup = BeautifulSoup(data, 'lxml', parse_only=strainer)
    product_name = soup.find('h1', attrs={"class": "wt-text-body-03 wt-line-height-tight wt-break-word wt-mb-xs-1"}).text.strip()
    product_image = soup.find('img', attrs={
        "class": "wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded",
        "data-index": "0"}).get('src')
    product_price = soup.find('p', attrs={"class": "wt-text-title-03 wt-mr-xs-2"}).text.strip()

    for formatting in ['$', '€', '£', '+', 'Price', ':', ' ']:
        if formatting in product_price:
            product_price = product_price.replace(formatting, '')

    new_product = Product(name=product_name, image=product_image, price=product_price)
    return new_product


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        product_link = request.form['url'].strip()
        if '?' in product_link:
            product_link = product_link.partition('?')[0]
        new_product = scrape_data(product_link)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occurred while adding the product'
    else:
        return render_template('search.html')


@app.route('/delete/<int:id>')
def delete(id):
    product_to_delete = Product.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/products')
    except:
        return 'An error occurred while deleting the product'

@app.route('/products')
def products():
    products = Product.query.order_by(Product.id).all()
    return render_template('products.html', products=products)

@app.route('/details/<int:id>')
def details(id):
    selected_product = Product.query.get_or_404(id)
    return render_template('details.html', product=selected_product)



if __name__ == "__main__":
    app.run(debug=True)