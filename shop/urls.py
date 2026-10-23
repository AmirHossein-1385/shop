from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
app_name = 'shop'

urlpatterns = [
    path('products/',views.product_list,name='product_list'),
    path('products/<slug:category_slug>/',views.product_list,name='products_list_by_category'),
    path('products/<int:id>/<slug:slug>/',views.product_detail,name='product_detail'),
    path('cheapest-products/',views.cheapest_product,name='cheapest_product'),
    path('expensive products/',views.expensive_products,name='expensive_products'),
    path('latest-products/',views.latest_products,name='latest_products'),
    path('filter-products/',views.filter_products,name='filter_products'),
    path('list-saved-product/',views.list_saved_products,name='list_saved_product'),
    path('save-product/<int:product_id>',views.save_product,name='save_product'),
    path('apply-code/',views.apply_code,name='apply_code'),
    path('search/',views.search,name='search'),
    path('comment/<int:product_id>/',views.comment,name='comment'),
    path('best-sellers/',views.best_selling_products,name='best_selling_products'),
    path('discounted-products/',views.discounted_products,name='discounted_products'),
    path('discounted-products/<slug:category_slug>/',views.discounted_products,name='discounted_products_by_category'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
]