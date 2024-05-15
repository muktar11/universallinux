import genericpath
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from requests import request

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    CouponPurchase, CoursePurchaseCoupon, CoursePurchaseCoupon, Users, EmailSubscription, LNMOnline,
Course, Post, Video, CoursePurchaseRequest, Events,Books, )
from .serializers import (
    CouponPurchaseCouponSerializer, CouponPurchaseSerializer, CoursePurchaseSerializer, MyTokenObtainPairSerializer, RegisterSalesSerializer, LNMOnlineSerializer,
    RegisterStaffSerializer, StudentProfileUpdateSerializer,
    EmailSubscriptionSerializer, RegisterStudentSerializer,
   StudentCourseSerializer, CourseSerializer, PostSerializer, EventsSerializer,
    StudentProfileSerializer, VideoSerializer, 
    ResetPasswordSerializer, UsersSerializer, BooksSerializer, StudentEventSerializer,
)
from .permissions import (IsSalesOrReadOnly, IsStudentOrReadOnly, IsWebAdminOrReadOnly, IsTeacherOrReadOnly)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework import generics
from django.db.models import Q
from django.core.exceptions import FieldDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import cloudinary
from cloudinary.uploader import upload


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.get_user(request.data['email'])  # Get the user based on the provided email

        if isinstance(user, Users):
            response.data['last_name'] = user.last_name
        if isinstance(user, Users):
            response.data['first_name'] = user.first_name
        if isinstance(user, Users):
            response.data['id'] = user.id
        if isinstance(user, Users):
            response.data['is_student'] = user.is_student
        if isinstance(user, Users):
            response.data['is_sales'] = user.is_sales
        if isinstance(user, Users):
            response.data['is_teacher'] = user.is_teacher
        if isinstance(user, Users):
            response.data['isWebAdmin'] = user.isWebAdmin
           

        return response

    def get_user(self, email):
        try:
            return Users.objects.get(email=email)
        except Users.DoesNotExist:
            return None 

from rest_framework import serializers  # Add this import

class RegisterStudentView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method in ['PUT', 'POST']:
            return [AllowAny()]  # Only allow teachers to register
        else:
            return super().get_permissions()   
        
    def post(self, request):
        serializer = RegisterStudentSerializer(data=request.data) 
        if serializer.is_valid():
            user_data = serializer.save()
            user = user_data['user']  # Get the user instance
            response_data = {
                "message": "User registered successfully",
                "refresh": user_data['refresh'],
                "access": user_data['access'],
                "id": user.id,
                "is_student": user.is_student,
                "is_sales": user.is_sales,
                "is_teacher": user.is_teacher,
                "isWebAdmin": user.isWebAdmin
            }
            user_data = serializer
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        





class ConfirmRegistrationView(View):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def get(self, request, uidb64, token):
        self.check_permissions(request)
        user = RegisterStudentSerializer.confirm_registration(uidb64, token)
        if user:
            # Redirect to the sign-in page upon successful confirmation
            return redirect(reverse_lazy('sign-in'))
        else:
            return HttpResponse("Invalid confirmation link.")  

        
        
class RegisterStaffView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def post(self, request):
        self.check_permissions(request)
        serializer = RegisterStaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class RegisterSalesView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def post(self, request):
        self.check_permissions(request)
        serializer =  RegisterSalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
from django.core.exceptions import MultipleObjectsReturned
class RetrieveSalesView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()
        
    def get(self, request, pk):
        try:
            self.check_permissions(request)
            users = Users.objects.filter(sales_person_id=pk)
            serializer = UsersSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterEmailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()
        
    def post(self, request):
        self.check_permissions(request)
        serializer = EmailSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
import base64
import requests
from datetime import datetime
from django.http import JsonResponse
import json 

def get_access_token():
    secret = "zxbwLuBaQvRPQEo5WE7JyqiUeWQHYGWxyDi1Qv650hspWw04a0V3l6ISLiAdzfCj"
    consumer = "GtaxyQq50AJVSFQspjqVP96dR8p6rfRGGGkxnLOPPoBZ3gkS" 
    auth = (consumer, secret)
    headers = {'Content-Type': 'application/json'}
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        result = response.json()
        access_token = result['access_token']
        print(access_token)

        return access_token
    except requests.exceptions.RequestException as e:
        return str(e)

'''


'''
'''
'''
from django_daraja.mpesa.core import MpesaClient

class stk_push(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # Only allow authenticated users to make POST requests
        else:
            return super().get_permissions()
    def post(self, request):
        self.check_permissions(request)
        serializer = CoursePurchaseSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            phone = data.get("phone")
            amount = data.get("amount")
            client_id = data.get("client_id")
            course_id = data.get("course_id")            
            # Check if the purchase already exists
            existing_purchase = CoursePurchaseRequest.objects.filter(course_id=course_id, client_id=client_id).exists()
            if existing_purchase:
                print('You already bought this course')
                return Response({"error": "You have already bought this course."}, status=status.HTTP_400_BAD_REQUEST)

            # If the purchase does not exist, proceed with STK push
            else:
                # Assuming phone is formatted as '2547xxxxxxxx'
                cl = MpesaClient()
                phone = phone[1:]  
                account_reference = 'reference'
                transaction_desc = 'Description'
                callback_url = 'https://darajambili.herokuapp.com/express-payment';
                response = cl.stk_push(phone, amount, account_reference, transaction_desc, callback_url)
                return HttpResponse(response)
'''


from django_daraja.mpesa.core import MpesaClient
from django.http import JsonResponse 
class stk_push(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # Only allow authenticated users to make POST requests
        else:
            return super().get_permissions()
    def post(self, request):
        self.check_permissions(request)
        serializer = CoursePurchaseSerializer(data=request.data)
        if serializer.is_valid():
            # If the data is valid, save the validated data
            serializer.save()
            # Extract necessary fields from the validated data
            phone_number = serializer.validated_data.get('phone')
            amount = serializer.validated_data.get('amount')
            merchant_request_id = serializer.validated_data.get('MerchantRequestID')
            account_reference = 'reference'
            transaction_desc = 'Universal Online University'
            callback_url = 'https://darajambili.herokuapp.com/express-payment'
            # Perform the STK push operation with the extracted data
            cl = MpesaClient()
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            # Extract necessary information from the response object
            response_data = {
                'merchant_request_id': response.merchant_request_id,
                'checkout_request_id': response.checkout_request_id,
                'response_code': response.response_code,
                # Add other necessary fields here
            }        
            # Return the response data as JSON
            return JsonResponse({'response': response_data})
        else:
            # If the data is not valid, return validation errors
            return JsonResponse({'errors': serializer.errors}, status=400)
       
       
class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, "this is request.data")

        """
        {'Body':
            {'stkCallback':
             {
                'CheckoutRequestID': 'ws_CO_DMZ_401669274_11032019190235305',
                'MerchantRequestID': '19927-3244045-1',
                'ResultCode': 0,
                'ResultDesc': 'The service request is processed successfully.',
                'CallbackMetadata': {
                                        'Item': [
                                                {'Name': 'Amount', 'Value': 1.0},
                                                {'Name': 'MpesaReceiptNumber', 'Value': 'NCB1FW1DFZ'},
                                                {'Name': 'Balance'},
                                                {'Name': 'TransactionDate', 'Value': 20190311190244},
                                                {'Name': 'PhoneNumber', 'Value': 254718821114}
                                                ]
                                    }

                                    }
                }
        }

        """
        merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
        print(merchant_request_id, "this should be MerchantRequestID")
        checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = request.data["Body"]["stkCallback"]["ResultCode"]
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        print(amount, "this should be an amount")
        mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
        print(mpesa_receipt_number, "this should be an mpesa_receipt_number")
        balance = ""
        transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
        print(transaction_date, "this should be an transaction_date")
        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
        print(phone_number, "this should be an phone_number")
        from datetime import datetime
        str_transaction_date = str(transaction_date)
        print(str_transaction_date, "this should be an str_transaction_date")
        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")
        print(transaction_datetime, "this should be an transaction_datetime")
        import pytz
        aware_transaction_datetime = pytz.utc.localize(transaction_datetime)
        print(aware_transaction_datetime, "this should be an aware_transaction_datetime")
        from mpesa.models import LNMOnline
        our_model = LNMOnline.objects.create(
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            Amount=amount,
            ResultCode=result_code,
            ResultDesc=result_description,
            MpesaReceiptNumber=mpesa_receipt_number,
            Balance=balance,
            TransactionDate=aware_transaction_datetime,
            PhoneNumber=phone_number,
        )
        our_model.save()
        from rest_framework.response import Response
        return Response({"OurResultDesc": "YEEY!!! It worked!"})


class UpdateStudentView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def put(self, request,pk):
        self.check_permissions(request)
        user = Users.objects.get(_id=pk)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CouponPurchaseListCreateAPIView(APIView):
    def get(self, request):
        coupons = CoursePurchaseCoupon.objects.all() 
        serializer = CouponPurchaseCouponSerializer(coupons, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data 
        try: 
            coupon_code = data['coupon_code']
            # Check if the coupon exists
            if CouponPurchase.objects.filter(coupon_code=coupon_code).exists():
                # Coupon exists, proceed with purchase logic
                serializer = CouponPurchaseCouponSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Coupon does not exist, return an error response
                return Response({'error': 'Coupon does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            # Handle if 'coupon_code' is not found in the request data
            return Response({'error': 'Coupon code is required.'}, status=status.HTTP_400_BAD_REQUEST)

class CouponPurchaseRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(CoursePurchaseCoupon, pk=pk)

    def get(self, request, pk):
        coupon = self.get_object(pk)
        serializer = CouponPurchaseCouponSerializer(coupon)
        return Response(serializer.data)

    def put(self, request, pk):
        coupon = self.get_object(pk)
        serializer = CouponPurchaseCouponSerializer(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        coupon = self.get_object(pk)
        coupon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseRegisterView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()


    def post(self, request):
        self.check_permissions(request)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        self.check_permissions(request)
        course = Course.objects.all()
        serializer = CourseSerializer(course, many=True,  context={'request': request})
        return Response(serializer.data)



class CourseFilter(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields =  ['title', 'content', 'Instructor']

class StudentEventView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()
        
    def get(self, request, pk):
        try:
            self.check_permissions(request)
            event = Users.objects.get(id=pk)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudentEventSerializer(event, many=False, context={'request': request})
        return Response(serializer.data)
    
class EditCourseView(APIView):   
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()
        
    def get(self, request, pk):
        try:
            self.check_permissions(request)
            course = Course.objects.get(_id=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  
        serializer = CourseSerializer(course, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            self.check_permissions(request)
            course = Course.objects.get(_id=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            error_response = {
                "error": "Invalid data",
                "details": serializer.errors
            }
            print(error_response)  # Print the error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            self.check_permissions(request)
            course = Course.objects.get(_id=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostRegisterView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()  # Use default permissions for other methods
    def post(self, request):
        self.check_permissions(request)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        self.check_permissions(request)
        post = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(post, many=True,  context={'request': request})
        return Response(serializer.data)        
  
class CouponRegisterView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()

    def post(self, request):
        self.check_permissions(request)
        serializer = CouponPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            error_response = {
                "error": "Invalid data",
                "details": serializer.errors
            }
            print(error_response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            self.check_permissions(request)
            coupon_purchases = CouponPurchase.objects.all().order_by('-created_at')
            serializer = CouponPurchaseSerializer(coupon_purchases, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_response = {
                "error": "Internal server error",
                "details": str(e)  # Provide details of the exception for debugging purposes
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        try:
            self.check_permissions(request)
            coupon = CouponPurchase.objects.get(_id=pk)
        except CouponPurchase.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CouponPurchaseSerializer(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            error_response = {
                "error": "Invalid data",
                "details": serializer.errors
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try: 
            self.check_permissions(request)
            coupon = CouponPurchase.objects.get(_id=pk)
        except CouponPurchase.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        coupon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

class PostRegisterView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()

    def post(self, request):
        self.check_permissions(request)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            error_response = {
                "error": "Invalid data",
                "details": serializer.errors
            }
            print(error_response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        self.check_permissions(request)
        post = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(post, many=True, context={'request': request})
        return Response(serializer.data)
    
class BooksRegisterView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()
        
    def post(self, request):
        self.check_permissions(request)
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        self.check_permissions(request)
        post = Books.objects.all().order_by('-created_at')
        serializer = BooksSerializer(post, many=True,  context={'request': request})
        return Response(serializer.data)  
          
    def put(self, request, pk):
        try:
            self.check_permissions(request)
            book = Books.objects.get(_id=pk)
        except Books.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BooksSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            error_response = {
                "error": "Invalid data",
                "details": serializer.errors
            }
            print(error_response)  # Print the error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try: 
            self.check_permissions(request)
            book = Books.objects.get(_id=pk)
        except Books.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.http import JsonResponse
from django.core.serializers import serialize
import json
from rest_framework.parsers import FileUploadParser
class VideoRegisterView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()  # Use default permissions for other methods 

    def post(self, request):
        self.check_permissions(request)
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

    def get(self, request):
        videos = Video.objects.all().order_by('-created_at')
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)
       
    def put(self, request, pk):
        try:
            self.check_permissions(request)
            video = Video.objects.get(_id=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            error_response = {
                "error": "Invalid data",
                "details": serializer.errors
            }
            print(error_response)  # Print the error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try: 
            self.check_permissions(request)
            video = Video.objects.get(_id=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EditPostView(APIView):  
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def get(self, request, pk):
        try:
            self.check_permissions(request)
            post = Post.objects.get(_id=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  
        serializer = PostSerializer(post, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            self.check_permissions(request)
            post = Post.objects.get(_id=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            error_response = {
                "error": "Invalid data",
                "details": serializer.errors
            }
            print(error_response)  # Print the error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            self.check_permissions(request)
            post = Post.objects.get(_id=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        
class EventListView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()  # Use default permissions for other methods
        
    def get(self, request):
        self.check_permissions(request)
        events = Events.objects.all().order_by('-created_at')
        serializer = EventsSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        self.check_permissions(request)
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404


        
class EventDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def get_object(self, pk):
        return get_object_or_404(Events, id=pk)

    def get(self, request, pk):
        self.check_permissions(request)
        event = self.get_object(pk)
        serializer = EventsSerializer(event, context={'request': request})
        return Response(serializer.data)
    


    def put(self, request, pk):
        self.check_permissions(request)
        event = Events.objects.get(_id=pk)
        serializer = EventsSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.check_permissions(request)
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def get_queryset(self):
        # Retrieve queryset ordered by created_at in descending order
        return Events.objects.order_by('-created_at')


 


class EditEventView(APIView):  
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def get(self, request, pk):
        try:
            self.check_permissions(request)
            event = Events.objects.get(_id=pk)
        except Events.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  
        serializer = EventsSerializer(event, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            self.check_permissions(request)
            event = Events.objects.get(_id=pk)
        except Events.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EventsSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            error_response = {
                "error": "Invalid data",
                "details": serializer.errors
            }
            print(error_response)  # Print the error response
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            self.check_permissions(request)
            event = Events.objects.get(_id=pk)
        except Events.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_queryset(self):
        # Retrieve queryset ordered by created_at in descending order
        return Events.objects.order_by('-created_at')

class StudentProfileDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def get_object(self, pk):
        return get_object_or_404(Users, id=pk)

    def get(self, request, pk):
        self.check_permissions(request)
        student = self.get_object(pk)
        serializer = StudentProfileSerializer(student, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        self.check_permissions(request)
        student = self.get_object(pk)
        serializer =  StudentProfileUpdateSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.check_permissions(request)
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class StudentCourseDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()  
        
    def get(self, request, pk):  # Fix the method signature 
        self.check_permissions(request)
        student = Users.objects.filter(id=pk)
        serializer = StudentCourseSerializer(student, many=True,  context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        self.check_permissions(request)
        student = self.get_object(pk)
        serializer = StudentCourseSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.check_permissions(request)
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Users, Course
from .serializers import CourseSerializer

class BuyCourseView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def post(self, request, user_id, course_id):
        try:
            self.check_permissions(request)
            user = Users.objects.get(id=user_id)
            course = Course.objects.get(_id=course_id)
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is approved to buy a course and if they haven't already bought the same course
        if user:
            user.courses.add(course)
            return Response({"message": "Course bought successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not eligible to buy the course or already bought it"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, user_id):
        try:
            self.check_permissions(request)
            user = Users.objects.get(id=user_id)
            courses = user.courses.all()
            courses_serializer = CourseSerializer(courses, many=True, context={'request': request})
            return Response(courses_serializer.data)
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        self.check_permissions(request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']

            # Retrieve user
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate and set the new password
            user.set_password(new_password)
            user.save()

            # Send email notification
          #  subject = 'Your password has been reset'
          #  message = render_to_string('password_reset_email.html', {
          #      'user': user,
          #  })
          #  email = EmailMessage(subject, message, to=[user.email])
          #  email.send()

            return Response({"success": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentUserView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions()
        
    
    def get(self, request):  # Need to include 'request' as the first parameter
        users = Users.objects.filter(is_student=True)
        user_serializer = UsersSerializer(users, many=True)
        return Response(user_serializer.data)  # Accessing data attribute of the serializer

             
class StaffUserView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def get(self, request):  
        try:
            self.check_permissions(request)
            users = Users.objects.filter(is_teacher=True)  # Renamed 'user' to 'users' for better readability
            user_serializer = UsersSerializer(users, many=True)
            return Response(user_serializer.data)  # Accessing 'data' attribute of the serializer
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SalesUserView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Require authentication for retrieving course data
        elif self.request.method == 'PUT':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'POST':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        elif self.request.method == 'DELETE':
            return [IsWebAdminOrReadOnly()]  # Only allow teachers to register
        else:
            return super().get_permissions() 
        
    def get(self, request):  
        try:
            self.check_permissions(request)
            users = Users.objects.filter(is_sales=True)  # Renamed 'user' to 'users' for better readability
            user_serializer = UsersSerializer(users, many=True)
            return Response(user_serializer.data)  # Accessing 'data' attribute of the serializer
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)