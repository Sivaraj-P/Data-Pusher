from django.urls import path
from .views import AccountAPIView,DestinationAPIView,AccountDestinationAPIView,IncomingDataAPIView

urlpatterns=[
    path('accounts',AccountAPIView.as_view(),name='accounts'),
    path('accounts/<int:pk>',AccountAPIView.as_view(),name='accounts_pk'),
    path("destinations",DestinationAPIView.as_view(),name='destinations'),
    path("destinations/<int:pk>",DestinationAPIView.as_view(),name='destinations_pk'),
    path("account-destinations/<int:id>",AccountDestinationAPIView.as_view(),name="account_destinations"),
    path("server/incoming-data",IncomingDataAPIView.as_view(),name="incoming_data")
]