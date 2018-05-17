from django.conf.urls import url

from sample_app import views

urlpatterns = [
    url(r'^api/payments/token$', views.BrainTreeTokenAPIView.as_view()),
    url(r'^api/payments/pay$', views.PaymentAPIView.as_view())
]
