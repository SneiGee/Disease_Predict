# import operator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Symptom, Disease, DiseaseReport


def home(request):
    return render(request, 'index.html')


@method_decorator(login_required, name='dispatch')
class DashboardListView(ListView):
    template_name = 'dashboard.html'

    def get(self, request):
        symptoms = Symptom.objects.all()
        args = {'nbar': 'dashboard', 'symptoms': symptoms}
        return render(request, self.template_name, args)


@login_required
def search(request):
    symptom = Disease.objects.all()
    query = request.GET.get('q')
    if query:
        symptom = symptom.filter(
            Q(disease_name__icontains=query)
        ).distinct()
    args = {'symptom': symptom, 'nbar': 'dashboard'}
    return render(request, 'search.html', args)


@method_decorator(login_required, name='dispatch')
class EachDiseaseListView(ListView):
    model = Disease
    context_object_name = 'diseases'
    template_name = 'each_disease.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['symptom'] = self.symptom
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.symptom = get_object_or_404(Symptom, pk=self.kwargs.get('pk'))
        queryset = self.symptom.diseases.order_by('-disease_name')
        return queryset


@method_decorator(login_required, name='dispatch')
class SingleDiseaseListView(ListView):
    model = DiseaseReport
    context_object_name = 'diseasereport'
    template_name = 'single_disease.html'

    def get_context_data(self, **kwargs):
        session_key = 'viewed_disease_{}'.format(self.disease.pk)
        if not self.request.session.get(session_key, False):
            self.disease.views += 1
            self.disease.save()
            self.request.session[session_key] = True
        kwargs['disease'] = self.disease
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.disease = get_object_or_404(Disease, symptom__pk=self.kwargs.get('pk'), pk=self.kwargs.get('disease_pk'))
        queryset = self.disease.diseasereport.order_by('created_at')
        return queryset


@method_decorator(login_required, name='dispatch')
class DiseaseListView(ListView):
    template_name = 'view_disease.html'

    def get(self, request):
        diseases = Disease.objects.all()
        args = {'nbar': 'view_disease', 'diseases': diseases}
        return render(request, self.template_name, args)


@method_decorator(login_required, name='dispatch')
class MapListView(ListView):
    template_name = 'map.html'

    def get(self, request):
        args = {'nbar': 'map'}
        return render(request, self.template_name, args)


# class SearchListView(ListView):
#     """
#     Display a Blog List page filtered by the search query.
#     """
#     model = Disease
#     paginate_by = 10

#     def get_queryset(self):
#         qs = Disease.objects.filter()

#         keywords = self.request.GET.get('q')
#         if keywords:
#             query = SearchQuery(keywords)
#             title_vector = SearchVector('disease_name', weight='A')
#             content_vector = SearchVector('report', weight='B')
#             vectors = title_vector + content_vector
#             qs = qs.annotate(search=vectors).filter(search=query)
#             qs = qs.annotate(rank=SearchRank(vectors, query)).order_by('disease_name')

#         return qs


# def search(request):
#     query_string = ''
#     found_entries = None
#     if ('q' in request.GET) and request.GET['q'].strip():
#         query_string = request.GET['q']
#         entry_query = utils.get_query(query_string, ['disease_name', 'report', ])
#         diseases = Disease.objects.filter(entry_query).order_by('disease_name')
#         args = {
#             'query_string': query_string,
#             'diseases': diseases,
#             'nbar': 'dashboard'
#         }
#         return render(request, 'search.html', args)
#     else:
#         return render(request, 'search.html',
#                       {'query_string': 'Null', 'found_entries': 'Enter a search term',
#                                'nbar': 'dashboard'}
#                       )
