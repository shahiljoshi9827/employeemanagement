from rest_framework import serializers
from employee.models import Employee, AddressDetails, Qualification, WorkExperience, Projects


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressDetails
        fields = ('hno', 'street', 'city', 'state')


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ('qualificationName', 'percentage', 'fromDate', 'fromDate')


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ('companyName', 'fromDate', 'toDate', 'address')


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('title', 'description')


class AllDetailSerializer(serializers.ModelSerializer):
    addressdetail = serializers.SerializerMethodField()
    qualification = serializers.SerializerMethodField()
    workexperience = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'email', 'age', 'gender', 'phoneNo', 'photo', 'addressdetail', 'qualification',
            'workexperience',
            'projects')

    def get_addressdetail(self, obj):
        customer_account_query = AddressDetails.objects.get(
            employee_id=obj.id)
        serializer = AddressSerializer(customer_account_query)
        return serializer.data

    def get_qualification(self, obj):
        customer_account_query = Qualification.objects.filter(
            employee_id=obj.id)
        serializer = QualificationSerializer(customer_account_query, many=True)

        return serializer.data

    def get_projects(self, obj):
        customer_account_query = Projects.objects.filter(
            employee_id=obj.id)
        serializer = ProjectsSerializer(customer_account_query, many=True)

        return serializer.data

    def get_workexperience(self, obj):
        customer_account_query = WorkExperience.objects.filter(
            employee_id=obj.id)
        serializer = WorkExperienceSerializer(customer_account_query, many=True)

        return serializer.data

    def create(self, validated_data):
        employee = Employee.objects.create(**validated_data)

        addressdetail = self.context.get('addressdetail')
        AddressDetails.objects.create(hno=addressdetail.get('hno'), street=addressdetail.get('street'),
                                      city=addressdetail.get('city'), state=addressdetail.get('state'),
                                      employee=employee)

        qualification = self.context.get('qualification')
        for q in qualification:
            Qualification.objects.create(qualificationName=q.get('qualificationName'), percentage=q.get('percentage'),
                                         toDate=q.get('toDate'), fromDate=q.get('fromDate'), employee=employee)

        workexperience = self.context.get('workexperience')
        for w in workexperience:
            WorkExperience.objects.create(companyName=w.get('companyName'), fromDate=w.get('fromDate'),
                                          toDate=w.get('toDate'), address=w.get('address'), employee=employee)

        projects = self.context.get('projects')
        for p in projects:
            Projects.objects.create(title=p.get('title'), description=p.get('description'), employee=employee)

        return employee

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.email = validated_data.get('email')
        instance.age = validated_data.get('age')
        instance.gender = validated_data.get('gender')
        instance.phoneNo = validated_data.get('phoneNo')
        instance.save()

        AddressDetails.objects.filter(employee=instance).delete()
        Qualification.objects.filter(employee=instance).delete()
        WorkExperience.objects.filter(employee=instance).delete()
        Projects.objects.filter(employee=instance).delete()

        addressdetail = self.context.get('addressdetail')
        AddressDetails.objects.create(hno=addressdetail.get('hno'), street=addressdetail.get('street'),
                                      city=addressdetail.get('city'), state=addressdetail.get('state'),
                                      employee=instance)

        qualification = self.context.get('qualification')
        for q in qualification:
            Qualification.objects.create(qualificationName=q.get('qualificationName'), percentage=q.get('percentage'),
                                         toDate=q.get('toDate'), fromDate=q.get('fromDate'), employee=instance)

        workexperience = self.context.get('workexperience')
        for w in workexperience:
            WorkExperience.objects.create(companyName=w.get('companyName'), fromDate=w.get('fromDate'),
                                          toDate=w.get('toDate'), address=w.get('address'), employee=instance)

        projects = self.context.get('projects')
        for p in projects:
            Projects.objects.create(title=p.get('title'), description=p.get('description'), employee=instance)

        return instance
