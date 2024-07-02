from django.http import JsonResponse


def hello(request):
    return JsonResponse({"message": "Thank you for using this application!"})
