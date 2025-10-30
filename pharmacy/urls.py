from django.urls import path
from . import views

app_name = "pharmacy"

urlpatterns = [
    path("", views.home, name="home"),  # ✅ home sahifa
    path("search/", views.search_page, name="search"),  # 🔄 qidiruv sahifasi endi /search/
    path("medicine/<slug:slug>/", views.medicine_detail, name="medicine_detail"),
    path("pharmacy/<int:pk>/", views.pharmacy_detail, name="pharmacy_detail"),
    path("api/search/", views.MedicineSearchView.as_view(), name="api_search"),
    path("api/nearby/", views.NearbyPharmaciesView.as_view(), name="api_nearby"),
    path("api/medicine/<slug:slug>/", views.MedicineDetailAPI.as_view(), name="api_medicine"),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),  # ✅ bu yangi qo‘shiladi
]
