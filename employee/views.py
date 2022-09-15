from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from employee.models import Employee, AddressDetails, Qualification, WorkExperience, Projects
from employee.serializers import AllDetailSerializer


class EmployeeList(APIView):
    """
    List all Employees, or create a new Employee.
    """

    def get(self, request, format=None):
        if request.query_params.get("regid"):
            regid = request.query_params.get("regid")

            try:
                employee = Employee.objects.get(id=regid.split("EMP")[1])
                serializer = AllDetailSerializer(employee)
                data = {
                    "messsage": "employee details found",
                    "success": True,
                    "employees": serializer.data

                }
                return Response(data=data, status=status.HTTP_200_OK)

            except (ObjectDoesNotExist, AttributeError):
                error = {
                    "message": f"no employee found with this {regid}",
                    "success": False
                }
                return Response(data=error, status=status.HTTP_200_OK)

        try:
            employees = Employee.objects.all()
            serializer = AllDetailSerializer(employees, many=True)
            data = {
                "messsage": "employee details found",
                "success": True,
                "employees": serializer.data

            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception:
            data = {
                "messsage": "employee details not found",
                "success": False,
                "employees": []
            }
            return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            serializer = AllDetailSerializer(data=request.data,
                                             context={"addressdetail": request.data.get('addressdetail'),
                                                      "qualification": request.data.get('qualification'),
                                                      "workexperience": request.data.get(
                                                          'workexperience'),
                                                      "projects": request.data.get('projects')})

            if serializer.is_valid():
                serializer.save()
                data = {
                    "message": "employee created successfully",
                    "regid": f"EMP{serializer.data.get('id')}",
                    "success": True,
                }
                return Response(data=data, status=status.HTTP_201_CREATED)
            error = {
                "message": "invalid body request",
                "success": False
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = {
                "message": "employee created failed",
                "success": False
            }
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeDetail(APIView):
    """
    Retrieve, update or delete a Employee instance.
    """

    def get(self, request, pk, format=None):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = AllDetailSerializer(employee)
            data = {
                "messsage": "employee details found",
                "success": True,
                "employees": serializer.data

            }
            return Response(data=data, status=status.HTTP_200_OK)

        except (ObjectDoesNotExist, AttributeError):
            error = {
                "message": f"no employee found with this EMP{pk}",
                "success": False
            }
            return Response(data=error, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            try:
                employee = Employee.objects.get(pk=pk)
            except (ObjectDoesNotExist, AttributeError):
                error = {
                    "message": f"no employee found with this EMP{pk}",
                    "success": False
                }
                return Response(data=error, status=status.HTTP_200_OK)
            serializer = AllDetailSerializer(employee, data=request.data,
                                             context={"addressdetail": request.data.get('addressdetail'),
                                                      "qualification": request.data.get('qualification'),
                                                      "workexperience": request.data.get('workexperience'),
                                                      "projects": request.data.get('projects')})
            if serializer.is_valid():
                serializer.save()
                data = {'message': 'employee details updated successfully',
                        'success': True
                        }

                return Response(data=data, status=status.HTTP_200_OK)
            error = {
                "message": f"invalid body request {str(serializer.errors)}",
                "success": False
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = {
                "message": f"employee updation failed {str(e)}",
                "success": False
            }
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        try:
            try:
                employee = Employee.objects.get(pk=pk)
            except ObjectDoesNotExist:
                error = {
                    "message": f"no employee found with this EMP{pk}",
                    "success": False
                }
                return Response(data=error, status=status.HTTP_200_OK)
            employee.delete()
            AddressDetails.objects.filter(employee_id=pk).delete()
            Qualification.objects.filter(employee_id=pk).delete()
            WorkExperience.objects.filter(employee_id=pk).delete()
            Projects.objects.filter(employee_id=pk).delete()
            data = {
                "message": "employee deleted successfully",
                "success": True
            }

            return Response(data=data, status=status.HTTP_200_OK)
        except Exception:
            error = {
                "message": "employee deletion failed",
                "success": False
            }
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
