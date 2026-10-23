from shop.models import Product, DiscountCode


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            if self.cart[product_id]['quantity'] < product.inventory:
                self.cart[product_id]['quantity'] += 1
        self.save()


    def decrease(self,product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()


    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()


    def clear(self):
        del self.session['cart']
        self.save()


    def get_post_price(self):
        weight = sum(item['weight'] + item['quantity'] for item in self.cart.values())
        if weight < 1000:
            return 20000
        elif 1000<=weight<=2000:
            return 30000
        else:
            return 50000


    def get_total_price(self):
        # price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        price = sum(Product.objects.get(id=product_id).new_price * item['quantity'] for product_id,item in self.cart.items())
        return price

    def get_final_price(self):
        total_price = self.get_total_price()
        discount_code = self.session.get('discount_code')

        if discount_code:
            discount_obj = DiscountCode.objects.filter(code=discount_code).first()

            if discount_obj:
                discount = discount_obj.discount
                total_price = total_price * (100 - discount) // 100
            else:
                del self.session['discount_code']

        return total_price + self.get_post_price()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        card_dict = self.cart.copy()
        for product in products:
            card_dict[str(product.id)]['product'] = product

        for item in card_dict.values():
                item['total'] = item['product'].new_price * item['quantity']
                yield item


    def save(self):
        self.session.modified = True

