from .models import Category, Brand, Product

def category_menu(request):

    categories = Category.objects.all()

    menu = []

    for category in categories:

        brand_ids = Product.objects.filter(category=category).values_list("brand_id",flat=True).distinct()

        brands = Brand.objects.filter(
            id__in=brand_ids
        )

        menu.append({
            "category": category,
            "brands": brands
        })

    return {
        "category_menu": menu
    }