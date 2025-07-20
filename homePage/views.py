from collections import OrderedDict

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from rest_framework.parsers import JSONParser
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from homePage.models import *
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from django.core.paginator import Paginator
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.core.mail import send_mail
from BookStore import settings
# Create your views here.

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


def checkIfUserIsAuthenticated(REQUEST) :
    if REQUEST.COOKIES.get('refresh') or REQUEST.COOKIES.get('sessionid') :
        return True
    else :
        return False


def extract_url_param(REQUEST) :
     referer_url = REQUEST.META.get('HTTP_REFERER')
     # Parse the URL
     parsed_url = urlparse(referer_url)

     # Extract the path (e.g., "/book/123/")
     path = parsed_url.path

     # Split the path to get the book_id
     parts = path.split('/')

     # The book_id is the second part (e.g., ["", "book", "123", ""])
     if len(parts) >= 3 and parts[1] == 'book':
         return parts[2]  # Return the book_id
     return None

def total_user_cost(user):
     cartItems = CartItem.objects.filter(user=user)
     price = 0
     for item in cartItems :
          price += item.book.price * item.count
     return create_thousand_separator(price+40000)

def total_user_books_price(user):
     cartItems = CartItem.objects.filter(user=user)
     price = 0
     for item in cartItems :
          price += item.book.price * item.count
     return create_thousand_separator(price)


def total_user_books_price_in_digits(user):
    cartItems = CartItem.objects.filter(user=user)
    price = 0
    for item in cartItems:
        price += item.book.price * item.count
    return price

def one_item_total_count(user,bookModel):
    cartItem = CartItem.objects.get(user=user,book=bookModel)
    price = cartItem.book.price * cartItem.count
    return create_thousand_separator(price)



def homePageContents() :
    categories = Category.objects.all()
    books = Book.objects.all()[0:8]
    return {
        'categories': categories,
        'books': books
    }


def homeRender(request):
              context = homePageContents()
              userNavBar = render_to_string('notValidUser-header.html', request=request)
              context['nav'] = userNavBar
              return render(request, 'homePage.html', context)


def homeAuthRender(request) :
              context = homePageContents()
              userNavBar = render_to_string('validUser-header.html', request=request)
              context['nav'] = userNavBar
              return render(request, 'homePage.html', context)


def get_search_result(request) :
    data = JSONParser().parse(request)
    searchExpression = data['inputValue']
    books = Book.objects.all()
    foundBooks = {

    }
    for book in books :
         if searchExpression in book.author or searchExpression in book.bookName :
             foundBooks[str(book.id)] = {
                 'name' : book.bookName,
                 'author' : book.author
             }
    return JsonResponse(foundBooks)

def get_books_by_filter(request,filter) :
     if filter == 'all' :
          books = Book.objects.all()[0:7]
     elif filter == 'newest' :
          books = Book.objects.all().order_by('-created_at')[0:7]
     elif filter == 'mostSell' :
          books = Book.objects.all().order_by('-sell_count')[0:7]
     elif filter == 'hotDeal' :
          books = Book.objects.filter(hotDeal=True)[0:7]

     jsonReturn = []
     for book in books :
          jsonReturn.append({
              'id' : book.id ,
              'name' : book.bookName,
              'author' : book.author,
              'price' : create_thousand_separator(book.price) ,
              'image-url' : book.image.url
          })
     return JsonResponse(jsonReturn,safe=False)

def bookView(request,bookID) :
    if checkIfUserIsAuthenticated(request) :
         fragment = render_to_string('comment-submit.html',request=request)
         nav = render_to_string('validUser-header.html', request=request)
    else :
         fragment = render_to_string('you-should-login.html' , request=request)
         nav = render_to_string('notValidUser-header.html', request=request)

    book = Book.objects.get(id=bookID)
    categories = book.category.all()
    relatedBooks = []
    for x in categories :
        query = Book.objects.filter(category=x.id)
        for item in query :
            if item != book:
                relatedBooks.append(item)

    relatedBooks = list(set(relatedBooks[0:4]))
    comments = Comment.objects.filter(relatedBook=book)
    return render(request, 'Book.html', {'book': book ,'commentFragment' : fragment,'comments' : comments , 'nav' : nav , 'relatedBooks' : relatedBooks })



def commentSubmit(request) :
     book_id = extract_url_param(request)
     content = request.POST['content']
     token = request.COOKIES.get('refresh')
     sessionID = request.COOKIES.get('sessionid')
     if token :
              user_id = RefreshToken(token)['user_id']
              user = MyUser.objects.get(id=user_id)
     elif sessionID :
               user = request.user

     comment = Comment.objects.create(bodyText=content,author=user,relatedBook=Book.objects.get(id=book_id))
     comment.save()
     messages.success(request, 'کامنت شما ثبت شد')
     return redirect(request.META['HTTP_REFERER'])


def addToFav(request,bookID) :
    token = request.COOKIES.get('refresh')
    sessionID = request.COOKIES.get('sessionid')
    if token:
        user_id = RefreshToken(token)['user_id']
        user = MyUser.objects.get(id=user_id)
    elif sessionID:
        user = request.user
    else :
        messages.error(request,'ابتدا وارد شوید یا ثبت نام کنید')
        return redirect(request.META['HTTP_REFERER'])

    book = Book.objects.get(id=bookID)
    for x in user.favBooks.all() :
         if x.bookName == book.bookName :
             messages.error(request,'کتاب از قبل در لیست علاقه مندی ها وجود دارد')
             return redirect(request.META['HTTP_REFERER'])

    user.favBooks.add(book)
    messages.success(request,'کتاب مورد نظر به لیست علاقه مندی های شما اضافه شد')
    return redirect(request.META['HTTP_REFERER'])

def delFromFav(request,bookID) :
    token = request.COOKIES.get('refresh')
    sessionID = request.COOKIES.get('sessionid')
    if token:
        user_id = RefreshToken(token)['user_id']
        user = MyUser.objects.get(id=user_id)
    elif sessionID:
        user = request.user

    book = Book.objects.get(id=bookID)
    user.favBooks.remove(book)
    messages.success(request, 'کتاب مورد نظر از لیست علاقه مندی ها حذف شد')
    return redirect(request.META['HTTP_REFERER'])

def addToCart(request,bookID) :
    token = request.COOKIES.get('refresh')
    sessionID = request.COOKIES.get('sessionid')
    if token:
        user_id = RefreshToken(token)['user_id']
        user = MyUser.objects.get(id=user_id)
    elif sessionID:
        user = request.user
    else :
        messages.error(request,'ابتدا وارد شوید یا ثبت نام کنید')
        return redirect(request.META['HTTP_REFERER'])

    book = Book.objects.get(id=bookID)
    try : query = CartItem.objects.filter(user=user)
    except CartItem.DoesNotExist: query = []
    for x in query :
         if x.book.bookName == book.bookName :
             messages.error(request,'کتاب از قبل در سبد خرید شما موجود است')
             return redirect(request.META['HTTP_REFERER'])

    cartItem = CartItem(book=book,user=user)
    cartItem.save()
    messages.success(request,'کتاب مورد نظر به سبد خرید شما اضافه شد')
    return redirect(request.META['HTTP_REFERER'])


def category_view(request,catID) :
    if checkIfUserIsAuthenticated(request):
        nav = render_to_string('validUser-header.html', request=request)
    else:
        nav = render_to_string('notValidUser-header.html', request=request)

    category = Category.objects.get(id=catID)
    books = Book.objects.filter(category__id=int(catID))
    filter = request.GET.get('filter')
    availability = request.GET.get('availability')
    if filter == 'new' :
         books = books.order_by('-created_at')
    if filter == 'most' :
         books = books.order_by('-sell_count')
    if filter == 'deal' :
         books = books.exclude(hotDeal=False)

    if availability == 'True' :
         books = books.exclude(is_available=False)

    p = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_number_int = int(page_number)
    diff = p.num_pages - page_number_int
    if page_number_int - 5 <= 0 :
        backPage = 1
    else :
        backPage = page_number_int - 5
    if diff < 5 :
        step = range(page_number_int , page_number_int + diff + 1)
    else :
         step = range(page_number_int , page_number_int + 5)
    books = p.get_page(page_number)
    return render(request,'Category.html',{'books' : books , 'nav' : nav , 'category' : category  , 'step' : step , 'filter' : filter , 'backPage' : backPage })

def profile_view(request):
  try :
    token = request.COOKIES.get('refresh')
    sessionID = request.COOKIES.get('sessionid')

    if checkIfUserIsAuthenticated(request):
        nav = render_to_string('validUser-header.html', request=request)
    else:
        nav = render_to_string('notValidUser-header.html', request=request)

    if token:
        user_id = RefreshToken(token)['user_id']
        user = MyUser.objects.get(id=user_id)
    elif sessionID:
        user = request.user

    favBooks = user.favBooks.all()

    return render(request , 'user-profile.html' , {'nav' : nav , 'favBooks' : favBooks , 'user' : user})

  except Exception as e :
    messages.error(request, 'لطفا ابتدا ثبت نام خود را مجددا و به طور کامل انجام دهید')
    return redirect('/profile/logout')


def profile_logout(request) :

  try :
     session_id = request.COOKIES.get('sessionid')
     refresh_token = request.COOKIES.get('refresh')
     access_token = request.COOKIES.get('access')

     if session_id :
           request.session.flush()
           return redirect('/')
     if not session_id and refresh_token:
           user_tokens = OutstandingToken.objects.filter(user=request.user.id)
           user_tokens.delete()
           response = HttpResponseRedirect('/')
           response.delete_cookie('refresh')
           if access_token : response.delete_cookie('access')
           return response


     # if user didn't log in , it will be back to the home
     return redirect('/')

  except Exception as e :
      messages.error(request, 'something went wrong')
      return redirect(request.META['HTTP_REFERER'])


def profile_completion_view(request) :

    token = request.COOKIES.get('refresh')
    sessionID = request.COOKIES.get('sessionid')
    if token:
        user_id = RefreshToken(token)['user_id']
        user = MyUser.objects.get(id=user_id)
    elif sessionID:
        user = request.user

    try :
         user.uniqueMail = request.POST.get('uniqueMail')
         user.username = request.POST.get('username')
         user.phoneNumber = request.POST.get('phoneNumber')
         user.full_clean()
         user.save()
         messages.success(request,'اطلاعات شما با موفقیت تغییر کرد')
    except (Exception,ValidationError) as e:
        if 'phoneNumber' in e.message_dict:
            messages.error(request, 'شماره همراه وارد شده معتبر نیست')
        else : messages.error(request,f'ایمیل یا نام کاربری از قبل وجود دارد')

    return redirect(request.META['HTTP_REFERER'])


def about_us(request) :
   if request.method == 'GET' :
            if checkIfUserIsAuthenticated(request):
                nav = render_to_string('validUser-header.html', request=request)
            else :
                nav = render_to_string('notValidUser-header.html' , request=request)
            return render(request ,'about-us.html' , {'nav' : nav })
   if request.method == 'POST' :
        commentAuthor = request.POST.get('username')
        authorEmail = request.POST.get('email')
        bodyText = request.POST.get('bodyText')
        try:
            send_mail(
                f'arrived comment from {commentAuthor}',
                f'{bodyText}',
                settings.EMAIL_HOST_USER,
                ['mahdishafaati4029@gmail.com']
            )
            messages.success(request,'ایمیل با موفقیت ارسال شد')
            return redirect(request.META['HTTP_REFERER'])
        except Exception as e :
            messages.error(request,f'{e}')
            return redirect(request.META['HTTP_REFERER'])


def shopping_cart(request) :

  try :
    token = request.COOKIES.get('refresh')
    sessionID = request.COOKIES.get('sessionid')
    if token:
        user_id = RefreshToken(token)['user_id']
        user = MyUser.objects.get(id=user_id)
    elif sessionID:
        user = request.user
    if checkIfUserIsAuthenticated(request):
        nav = render_to_string('validUser-header.html', request=request)
    else:
        nav = render_to_string('notValidUser-header.html', request=request)
    try:
        shopList = CartItem.objects.filter(user=user)
    except Exception as e :
        shopList = None

    return render(request, 'cart.html', {'nav': nav, 'shopList': shopList, 'user': user})


  except Exception as e :
         messages.error(request, 'لطفا ابتدا ثبت نام کنید یا وارد شوید')
         return redirect(request.META['HTTP_REFERER'])




def create_address_error(request):
    messages.error(request,'لطفا فرم مربوطه به مشخصات ارسال را در انتهای صفحه پر کنید')
    return HttpResponse(status=200)


def remove_from_cart(request,bookId):
       token = request.COOKIES.get('refresh')
       sessionID = request.COOKIES.get('sessionid')
       if token:
           user_id = RefreshToken(token)['user_id']
           user = MyUser.objects.get(id=user_id)
       elif sessionID:
           user = request.user
       book = Book.objects.get(id=bookId)
       cartItem = CartItem.objects.get(book=book,user=user)
       removed_price = cartItem.book.price * cartItem.count
       price = total_user_books_price_in_digits(user)
       price = price - removed_price
       total_cost = price + 40000
       cartItem.delete()
       return JsonResponse({'all_books' : create_thousand_separator(price) , 'all_cost' : create_thousand_separator(total_cost)},status=200)

def insert_item_count(request) :
    token = request.COOKIES.get('refresh')
    sessionID = request.COOKIES.get('sessionid')
    if token:
        user_id = RefreshToken(token)['user_id']
        user = MyUser.objects.get(id=user_id)
    elif sessionID:
        user = request.user
    book = Book.objects.get(id=request.GET.get('id'))
    count = int(request.GET.get('count'))
    cartItem = CartItem.objects.get(book=book,user=user)
    cartItem.count = count
    cartItem.save()
    sumPrice = create_thousand_separator(cartItem.book.price * count)

    return JsonResponse({'item' : sumPrice ,
                              'all_books' : total_user_books_price(user),
                              'all_cost' : total_user_cost(user)
                         },status=200)


def create_order(request):
    token = request.COOKIES.get('refresh')
    sessionID = request.COOKIES.get('sessionid')
    if token:
        user_id = RefreshToken(token)['user_id']
        user = MyUser.objects.get(id=user_id)
    elif sessionID:
        user = request.user
    data = JSONParser().parse(request)
    address = data['address']
    customerName = data['username']
    order = Order(address=address, customerName=customerName, user=user)
    order.save()
    return JsonResponse({'orderAddress' : order.address , 'orderCustomer' : order.customerName})
