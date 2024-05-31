from django.db import models
import uuid

# Create your models here.


class Bank(models.Model):

    uuid=models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True)

    bank_id=models.CharField(max_length=255,unique=True)

    name=models.CharField(max_length=255,unique=True)


    def __str__(self):
        return self.name
    

class Branch(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4,primary_key=True)
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE,related_name="branch")

    ifsc_code=models.CharField(max_length=255,unique=True)

    branch=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    district=models.CharField(max_length=255)
    state=models.CharField(max_length=255)


    def __str__(self):

        return self.branch+self.ifsc_code
