from django.shortcuts import render


def start_page_open_ai(request):
    return render(request, 'open_ai_start.html')
