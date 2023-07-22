"""
Restframework imports
"""
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework.response import Response

"""
other imports
"""

import math
from utils import json

"""
Django imports
"""
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

class CustomPagination1(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        page=data["pageno"]
        page_size = data["pagelimit"]
        paginator = Paginator(data["datas"],page_size)
        return {
                'total_count':math.ceil(int(paginator.count)),
                'totalPageNo': math.ceil(int(paginator.count)/int(page_size)),
                'perPage': int(self.request.GET.get('page_size', page_size)),
                'currentPageNo': int(self.request.GET.get('page', page)), # can not set default = self.page
                "data":data["datas"] 
        }

class CustomPagination(LimitOffsetPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        page=data["pageno"]
        page_size = data["pagelimit"]   
        paginator = Paginator(data["datas"],page_size)
        return {
                'total_count':math.ceil(int(paginator.count)),
                'totalPageNo': math.ceil(int(paginator.count)/int(page_size)),
                'perPage': int(self.request.GET.get('page_size', page_size)),
                'currentPageNo': int(self.request.GET.get('page', page)), # can not set default = self.page
                "data":data["datas"],
                "next":self.get_next_link(),
                'previous': self.get_previous_link()
        }

"""
custom pagination
"""
def pagination_class(data,request,count):
    try:
        page=request.query_params.get('page')
        page_size=request.query_params.get('item')
        # page=int(page)+0

        paginator = Paginator(data,page_size)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(1)
        
        return {
                'total_count':count,
                'totalPageNo': math.ceil(int(count)/int(page_size)),
                'perPage': int(request.GET.get('page_size', page_size)),
                'currentPageNo': int(request.GET.get('page', page)), # can not set default = self.page
                "data":list(users)
        }
    except:
        raise Exception

# class CustomPagination(PageNumberPagination):
#     page = DEFAULT_PAGE
#     page_size = DEFAULT_PAGE_SIZE
#     page_size_query_param = 'page_size'

#     def get_paginated_response(self, data):
#         return {
#                 'total_count':math.ceil(int(self.page.paginator.count)),
#                 'totalPageNo': math.ceil(int(self.page.paginator.count)/int(self.page_size)),
#                 'perPage': int(self.request.GET.get('page_size', self.page_size)),
#                 'currentPageNo': int(self.request.GET.get('page', DEFAULT_PAGE)), # can not set default = self.page
#                 "data":data 
#         }
def test_pagination(offset,limit,page):
    if page == 1:
        offset = offset
        limit = limit
    if page !=1:
        offset = (int(page) -1) * int(limit)
        # offset +=1
        limit = (int(limit) * int(page))
    
    return offset,limit

def pagination_calculation(query,pagelimit):
    total_count=query
    count_1 = total_count % pagelimit
    count_2 = total_count // pagelimit
    if  count_1 != 0:
        count_2 +=1
    return total_count,count_2