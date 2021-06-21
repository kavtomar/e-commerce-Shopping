from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Shophome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('products/<int:myid>', views.productView, name="ProductView"),
    path('checkout/', views.checkout, name="Checkout"),
    path("privacy/", views.privacy, name="PrivacyPolicy"),
    path("faq/", views.faq, name="FAQs"),
    path("watches/", views.watches, name="watches"),
    path('fashion/', views.fashion, name='fashionwears'),
    path('footwears/', views.footwears, name='fashionwears'),
    path('electronics/', views.electronics, name='electronics'),
     path('households/', views.households, name='households'),
    path('households/', views.households, name='households'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),


]