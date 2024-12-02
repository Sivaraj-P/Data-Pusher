from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Account,Destination
from .serializers import AccountSerializer,DestinationSerializer
import requests

class AccountAPIView(APIView):

    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         self.permission_classes = [AllowAny]
    #     return [permission() for permission in self.permission_classes]


    def get(self, request,pk=None):
        
        if pk:
            try:
                queryset=Account.objects.get(pk=pk)
            except Account.DoesNotExist:
                return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = AccountSerializer(queryset)
        else:
            queryset=Account.objects.all()
            serializer = AccountSerializer(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):

        try:
            queryset=Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AccountSerializer(data=request.data,instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request,pk):
        try:
            queryset=Account.objects.get(pk=pk)
            queryset.delete()
            return Response({"message": "Account deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        

class DestinationAPIView(APIView):
    def get(self, request,pk=None):
        if pk:
            try:
                destinations = Destination.objects.get(pk=pk)
                serializer = DestinationSerializer(destinations)
            except Destination.DoesNotExist:
                return Response({"error": "Destination not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            destinations = Destination.objects.all()
            serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        try:
            destinations = Destination.objects.get(pk=pk)
            serializer = DestinationSerializer(data=request.data,instance=destinations)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Account.DoesNotExist:
            return Response({"error": "Destination not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            destination = Destination.objects.get(pk=pk)
            destination.delete()
            return Response({"message": "Destination deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Destination.DoesNotExist:
            return Response({"error": "Destination not found"}, status=status.HTTP_404_NOT_FOUND)


class AccountDestinationAPIView(APIView):
    def get(self,request,id):
        queryset=Destination.objects.filter(account_id=id)
        serializer = DestinationSerializer(queryset, many=True)
        return Response(serializer.data)


from .permission import AuthUser

#  AuthUser permission class validates the secret token and store the account instance in request obj

class IncomingDataAPIView(APIView):
    permission_classes=[AuthUser]
    def post(self, request):
        data = request.data
        account = request.account  
        for destination in account.destinations.all():
    
            try:
                if destination.http_method == 'GET':
                    requests.get(destination.url, headers=destination.headers, params=data)
                elif destination.http_method =="POST":
                    requests.post( destination.url, headers=destination.headers, json=data)
                elif destination.http_method =="PUT":
                    requests.put( destination.url, headers=destination.headers, json=data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "Data sent to destinations"}, status=status.HTTP_200_OK)