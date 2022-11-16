from django.urls import path, include
from jaseci_serv.jsx_stripe.views import *

urlpatterns = [
    path("init/", StripeView.as_view(), name="stripe_init"),
]
