from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Country
from .serializers import CountrySerializer

class CountryPagination(PageNumberPagination):
    page_size = 5 
    page_size_query_param = 'page_size'
    max_page_size = 50

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = CountryPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name_common', 'name_official', 'capital', 'continent')
    ordering_fields = '__all__'
    ordering = ['name_common']

class CountryDetailView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
