
from store.models import Product
from decimal import Decimal


class Basket():
    """
    A base basket class, providing some default behaviors that can be inherted or overrided, as necessary
    """

    def __init__(self, request):
        # each request has a sessionn and this line sets the session of the request to the session of the basket
        self.session = request.session
        # the basket variable is set to value which is connected to the session key
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            # if the session key does not exist in the current session, the skey is set to an empty set
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id in self.basket:  # if the product id doesn't exist in the basket
            # a new value with the key of the product id will be added which inlcudes both price and quantity
            self.basket[product_id]['qty'] += qty
        else:
            self.basket[product_id] = {
                'price': str(product.price), 'qty': int(qty)}
        self.session.modified = True

    def delete(self, product):
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.session.modified = True


    def update(self, product, qty):
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.session.modified = True


    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
