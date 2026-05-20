from django.urls import path

from . import views

urlpatterns = [
    path("contact/", views.ContactSubmitView.as_view(), name="contact-submit"),
    path("newsletter/subscribe/", views.NewsletterSubscribeView.as_view(), name="newsletter-subscribe"),
]
