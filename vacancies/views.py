import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from vacancies.models import Vacancy


def hello(request):
    return HttpResponse("Hello world")


@method_decorator(csrf_exempt, name='dispatch')
class VacancyView(View):
    def get(self, request):
        search_key = request.GET.get('text')
        vacancies = Vacancy.objects.all()
        if search_key:
            vacancies = vacancies.filter(text__contains=search_key)

        response = [{'id': vacancy.id,
                     'text': vacancy.text}
                    for vacancy in vacancies]

        return JsonResponse(response, safe=False,
                            json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        vacancy = Vacancy(**json.loads(request.body))
        vacancy.save()
        return JsonResponse({'id': vacancy.id,
                             'text': vacancy.text}, status=201)


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()
        response = {'id': vacancy.id,
                    'text': vacancy.text}

        return JsonResponse(response, safe=False,
                            json_dumps_params={'ensure_ascii': False})
