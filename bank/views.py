from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from utils.csv_to_db import load_db
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from bank.models import Bank,Branch
from bank.serializers import BankSerializer,BranchSerializer

from utils.response import HTTP_200,HTTP_201,HTTP_400,HTTP_404


class DatabaseLoad(APIView):
    def get(self,request,*args,**kwargs):

        failed_rows=load_db()


        return HTTP_200(failed_rows)
    


class BanksAPIView(APIView):
    def get(self,request,*args,**kwargs):

        bank=Bank.objects.all()

        serializer=BankSerializer(bank,many=True)

        return HTTP_200(serializer.data)
    
class BanksDetailView(APIView):
    def get(self,request,*args,**kwargs):

        bank_uuid=kwargs.get('uuid',None)

        if not bank_uuid:
            return HTTP_400("Bank UUID is required.")
        

        try:
            bank=Bank.objects.get(uuid=bank_uuid)

        except Bank.DoesNotExist:
            return HTTP_404("Bank doesn't found")

        
        serializer=BankSerializer(bank)

        return HTTP_200(serializer.data)
    


    

class BranchesAPIView(APIView):
    def get(self,request,*args,**kwargs):

        branches=Branch.objects.all()

        
        pa=Paginator(branches,10)
        page=request.GET.get('page')
        
        page_object=pa.get_page(page)

        serializer=BranchSerializer(page_object,many=True)

        return HTTP_200(serializer.data)
    

class BranchesofBankAPIView(APIView):
    def get(self,request,*args,**kwargs):
        bank_uuid=kwargs.get('uuid',None)

        if not bank_uuid:

            return HTTP_400("Bank UUID is required.")
        

        branches=Branch.objects.filter(bank__uuid=bank_uuid)

        serializer=BranchSerializer(branches,many=True)


        return HTTP_200(serializer.data)
    


class BranchDetailAPIView(APIView):

    def get(self,request,*args,**kwargs):

        branch_uuid=kwargs.get('uuid',None)
        
        if not branch_uuid:
            return HTTP_400("Branch UUID is required")
        

        try:
            branch=Branch.objects.get(uuid=branch_uuid)
        except Branch.DoesNotExist:
            return HTTP_404("Branch doesn't found.")
        
        serializer=BranchSerializer(branch)

        return HTTP_200(serializer.data)


