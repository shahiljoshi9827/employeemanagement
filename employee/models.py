from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    phoneNo = models.CharField(max_length=12)
    photo = models.ImageField(upload_to='photos')

    def __str__(self):
        return f"EMP{self.id}"

    def id(self):
        return f"EMP{self.id}"


class AddressDetails(models.Model):
    hno = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.hno


class WorkExperience(models.Model):
    companyName = models.CharField(max_length=100)
    fromDate = models.DateField()
    toDate = models.DateField()
    address = models.CharField(max_length=200)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.companyName


class Qualification(models.Model):
    qualificationName = models.CharField(max_length=50)
    percentage = models.FloatField()
    toDate = models.DateField()
    fromDate = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.qualificationName


class Projects(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
