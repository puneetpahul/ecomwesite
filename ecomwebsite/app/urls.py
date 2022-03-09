from django.urls import path
from app import views

########## Image upload settings ###########
from django.conf import settings
from django.conf.urls.static import static
############################################

### login
from django.contrib.auth import views as  auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('', views.ProductView.as_view(),name= 'home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    
    path('buy/', views.buy_now, name='buy-now'),

    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),

    ##profile class based
    path('profile/', views.ProfileView.as_view(), name='profile'),

    ## mobile 
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    
    ## topwear
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),

    ## bottomwear
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),

    ## Laptop
    path('laptop/', views.laptop, name='laptop'),
    path('laptopwear/<slug:data>', views.laptop, name='laptopdata'),

    ## login prebuilt django url
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name = 'login'),

    ## logout builtin django url
    path('logout/',auth_views.LogoutView.as_view(next_page='home'),name = 'logout'),

    ## password change 
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class =MyPasswordChangeForm,success_url='/passwordchangedone/'),name = 'changepassword'),

    ##password change done
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/password_change_done.html'),name= 'passwordchangedone'),

    ## Password reset builtin
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name= 'password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name= 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name= 'password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name= 'password_reset_complete'),
    

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
