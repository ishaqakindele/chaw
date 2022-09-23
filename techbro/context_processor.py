from cartt.models import Shopcartt




def cartcount(request):
    count = Shopcartt.objects.filter(user__username = request.user.username, paid= False)

    itemcount= 0

    for item in count:
        itemcount += item.c_item

    context = {
        'itemcount': itemcount
    }

    return context