from rest_framework import serializers
from bank.models import Bank,Branch



class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model=Bank
        fields="__all__"

    

class BranchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Branch
        fields="__all__"
