from django.urls import path
from Pet import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home),
    path('details/<rid>',views.showPetDetails),
    path('register',views.registerUser),
    path('login',views.userLogin),
    path('logout',views.userLogout),
    path('addtocart/<pet_id>',views.addtocart),
    path('showCart',views.showUserCart),
    path('removepet/<cartid>',views.removeCart),
    path('updatecart/<opr>/<cartid>',views.updateCart),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)