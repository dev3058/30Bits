from django.urls import path
from .import views

# handler404 = 'url_shortner.views.custom_page_not_found_view'
# handler500 = 'url_shortner.views.custom_error_view'
# handler403 = 'url_shortner.views.custom_permission_denied_view'
# handler400 = 'url_shortner.views.custom_bad_request_view'

urlpatterns = [
    path('',views.shortner,name='shortner'),
    path('image_submission',views.image_handler,name="image_handler"),
    path('<slug:slug>',views.redirect_to_shortened, name='redirect'),
    path('url-details/<slug:slug>',views.url_details, name='url-details'),
    
]
