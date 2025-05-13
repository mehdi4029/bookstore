from django import template
from django.db.models import Sum
from homePage.models import CartItem

register = template.Library()


def create_thousand_separator(price) :
    price = str(price)
    start = len(price) - 3
    end = len(price) - 1
    finalStr = ''
    while start > 0:
        finalStr = ',' + price[start:end + 1] + finalStr
        start -= 3
        end -= 3
    return price[0:end + 1] + finalStr + '  تومان'


@register.filter
def total_user_cost(user):
     cartItems = CartItem.objects.filter(user=user)
     price = 0
     for item in cartItems :
          price += item.book.price * item.count
     return create_thousand_separator(price+40000)


@register.filter
def total_user_books_price(user):
     cartItems = CartItem.objects.filter(user=user)
     price = 0
     for item in cartItems :
          price += item.book.price * item.count
     return create_thousand_separator(price)



@register.filter
def one_item_total_count(user,bookModel):
    cartItem = CartItem.objects.get(user=user,book=bookModel)
    price = cartItem.book.price * cartItem.count
    return create_thousand_separator(price)
