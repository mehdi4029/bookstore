from django.urls import path
from homePage import views

# app_name = 'homePage'
urlpatterns = [
    path( "authHome", views.homeAuthRender, name="home" ),
    path("anonymousHome" , views.homeRender, name="anonymousHome"),
    path("book/<str:bookID>" , views.bookView , name="book" ),
    path("comment/submit" , views.commentSubmit , name="comment" ),
    path('fav/add/<str:bookID>' , views.addToFav , name="addToFav" ),
    path('fav/delete/<str:bookID>' , views.delFromFav , name="delFromFav" ),
    path('cart/add/<str:bookID>' , views.addToCart , name="addToCart" ),
    path('category/<str:catID>' , views.category_view , name="category" ),
    path('profile/' , views.profile_view , name="profile" ),
    path('profile/logout' , views.profile_logout, name="logout" ),
    path('profile/completion' , views.profile_completion_view , name="profile_completion" ),
    path('about-us' , views.about_us , name="about_us" ),
    path('cart' , views.shopping_cart , name="shopping_cart" ),
    path('cart/remove/<str:bookId>' , views.remove_from_cart, name="remove_from_cart" ),
    path('cart/count/' , views.insert_item_count , name="insert_item_count" ),
    path('error/address' , views.create_address_error , name="create_address_error" ),
    path('order/create' , views.create_order , name="create_order" ),
    path('search/', views.get_search_result , name="get_search_result" ),
    path('getbook/<str:filter>' , views.get_books_by_filter , name="get_book_by_filter" ),
]