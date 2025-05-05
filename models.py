from django.db import models

class User(models.Model):
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=10)
    email=models.CharField(max_length=20)
    contact=models.CharField(max_length=10)
    img=models.ImageField(upload_to="media/",blank=True)
    class Meta:
        db_table="user"

class Expenses(models.Model):
    date=models.DateField()
    remark=models.CharField(max_length=50)
    amount=models.FloatField()
    catagory=models.CharField(max_length=10)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table="expense"

class Income(models.Model):
    date=models.DateField()
    remark=models.CharField(max_length=50)
    amount=models.FloatField()
    catagory=models.CharField(max_length=10)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table="income"

