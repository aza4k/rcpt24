from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Min, Q, Case, When
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Medicine, Pharmacy, Inventory,News
from .serializers import MedicineSearchSerializer, InventorySerializer, PharmacySerializer
from math import radians, sin, cos, asin, sqrt
from django.shortcuts import render


def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    latest_news = News.objects.exclude(id=news_item.id).order_by('-created_at')[:3]
    return render(request, 'pharmacy/news_detail.html', {
        'news_item': news_item,
        'latest_news': latest_news
    })


def home(request):
    popular_medicines = Medicine.objects.all()[:8]
    popular_pharmacies = Pharmacy.objects.all()[:6]
    latest_news = News.objects.order_by("-created_at")[:3]
    return render(request, "pharmacy/home.html", {
        "popular_medicines": popular_medicines,
        "popular_pharmacies": popular_pharmacies,
        "latest_news": latest_news,
    })


def search_page(request):
    q = request.GET.get("q", "").strip()
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    city = request.GET.get("city", "").strip()
    only_available = request.GET.get("available") == "1"

    inventories_qs = Inventory.objects.select_related("medicine", "pharmacy").all()

    if q:
        tokens = [t for t in q.split() if t]
        query_expr = Q()
        for token in tokens:
            token_q = Q(medicine__name__icontains=token) | Q(medicine__description__icontains=token)
            query_expr &= token_q
        inventories_qs = inventories_qs.filter(query_expr)

    if min_price:
        try:
            min_val = float(min_price)
            inventories_qs = inventories_qs.filter(price__gte=min_val)
        except (TypeError, ValueError):
            pass
    if max_price:
        try:
            max_val = float(max_price)
            inventories_qs = inventories_qs.filter(price__lte=max_val)
        except (TypeError, ValueError):
            pass

    if city:
        inventories_qs = inventories_qs.filter(pharmacy__address__icontains=city)

    if only_available:
        inventories_qs = inventories_qs.filter(quantity__gt=0)

    # Order by price with NULLs last
    inventories_qs = inventories_qs.order_by(Case(When(price__isnull=True, then=1), default=0), "price")

    paginator = Paginator(inventories_qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "inventories": page_obj.object_list,
        "page_obj": page_obj,
        "query": q,
    }
    return render(request, "pharmacy/search_results.html", context)

def medicine_detail(request, slug):
    medicine = get_object_or_404(Medicine, slug=slug)
    inventories = Inventory.objects.filter(medicine=medicine).select_related("pharmacy").order_by("price")
    return render(request, "pharmacy/medicine_detail.html", {"medicine": medicine, "inventories": inventories})

def pharmacy_detail(request, pk):
    pharmacy = get_object_or_404(Pharmacy, pk=pk)
    inventories = Inventory.objects.filter(pharmacy=pharmacy).select_related("medicine").order_by("medicine__name")
    return render(request, "pharmacy/pharmacy_detail.html", {"pharmacy": pharmacy, "inventories": inventories})

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

class MedicineSearchView(APIView):
    def get(self, request):
        q = request.GET.get("q", "").strip()
        if not q:
            return Response([])
        meds = (Medicine.objects.filter(name__icontains=q)
                .annotate(price_min=Min("inventory__price"), pharmacies_count=Count("inventory__pharmacy", distinct=True))
                .values("id", "name", "slug", "price_min", "pharmacies_count")[:20])
        return Response(list(meds))

class NearbyPharmaciesView(APIView):
    def get(self, request):
        try:
            lat = float(request.GET.get("lat"))
            lng = float(request.GET.get("lng"))
        except:
            return Response([])
        slug = request.GET.get("slug")
        medicine = Medicine.objects.filter(slug=slug).first() if slug else None
        invs = Inventory.objects.select_related("pharmacy", "medicine").all()
        if medicine:
            invs = invs.filter(medicine=medicine)
        results = []
        for inv in invs:
            ph = inv.pharmacy
            if ph.lat is None or ph.lng is None:
                continue
            d = haversine(lat, lng, ph.lat, ph.lng)
            results.append({
                "pharmacy_id": ph.id,
                "pharmacy": ph.name,
                "address": ph.address,
                "lat": ph.lat,
                "lng": ph.lng,
                "distance_km": round(d, 2),
                "price": float(inv.price) if inv.price is not None else None,
                "quantity": inv.quantity,
                "medicine": inv.medicine.name,
            })
        results.sort(key=lambda x: x["distance_km"])
        return Response(results)

class MedicineDetailAPI(APIView):
    def get(self, request, slug):
        medicine = get_object_or_404(Medicine, slug=slug)
        inventories = Inventory.objects.filter(medicine=medicine).select_related("pharmacy")
        serializer = InventorySerializer(inventories, many=True)
        data = {
            "name": medicine.name,
            "slug": medicine.slug,
            "description": medicine.description,
            "analogs": [a.strip() for a in medicine.analogs.split(",")] if medicine.analogs else [],
            "image": medicine.image.url if medicine.image else None,
            "inventories": serializer.data
        }
        return Response(data)


