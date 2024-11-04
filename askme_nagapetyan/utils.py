from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_objects(request, objects, per_page=5):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(1)
    return paginated_objects