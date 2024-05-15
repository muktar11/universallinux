from audioop import reverse
from base64 import urlsafe_b64encode
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Books, CouponPurchase, CoursePurchaseCoupon, CoursePurchaseRequest, Video,  EmailSubscription, Course, LNMOnline, CoursePurchaseRequest, Post, Events, Users 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model 
from django.contrib.auth.password_validation import validate_password
User = get_user_model()
import random
import string


    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Custom claims for Staff users
        if isinstance(user, Users):
            token['first_name'] = user.first_name 
        if isinstance(user, Users):
            token['last_name'] = user.last_name
        if isinstance(user, Users):
            token['id'] = user.id
        if isinstance(user, Users):
            token['is_student'] = user.is_student
        if isinstance(user, Users):
            token['is_sales'] = user.is_sales
        if isinstance(user, Users):
            token['is_teacher'] = user.is_teacher

        
        # Custom claims for WebCustomer users
        
        # Add more custom claims as needed
        # ...
        
        return token
'''
class RegisterStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = Users
        fields = '__all__'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone = validated_data['phone'],
            birthday = validated_data['birthday'],
            bio = validated_data['bio'],
            extracurricular = validated_data['extracurricular'],
            mda_imageuRL = validated_data['mda_imageUrl'],
            photo_imageUrl = validated_data['photo_imageUrl'],
            school_credentials_imageUrl = validated_data['school_credentials_imageUrl'],
            terms_and_agreement_imageUrl = validated_data['terms_and_agreement_imageUrl']
        )

        user.set_password(validated_data['password'])
        user.is_teacher=True
        user.save()

        return user
'''

class RegisterStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Users
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        password = ''.join(random.choices(string.digits, k=10))  # Generate random 10-digit password
        validated_data['password'] = password
        validated_data['password2'] = password
        user = Users.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone = validated_data['phone'],
            birthday = validated_data['birthday'],
            bio = validated_data['bio'],
            extracurricular = validated_data['extracurricular'],
            mda_imageUrl = validated_data['mda_imageUrl'],
            photo_imageUrl = validated_data['photo_imageUrl'],
            school_credentials_imageUrl = validated_data['school_credentials_imageUrl'],
            terms_and_agreement_imageUrl = validated_data['terms_and_agreement_imageUrl']
        )
        user.set_password(password)
        user.is_teacher = True
        user.save()
        
        # Handling many-to-many relationship
        
        return user




class RegisterSalesSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Users
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        password = ''.join(random.choices(string.digits, k=10))  # Generate random 10-digit password
        validated_data['password'] = password
        validated_data['password2'] = password
        user = Users.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone = validated_data['phone'],
            birthday = validated_data['birthday'],
            mda_imageUrl = validated_data['mda_imageUrl'],
            photo_imageUrl = validated_data['photo_imageUrl'],
            terms_and_agreement_imageUrl = validated_data['terms_and_agreement_imageUrl']
        )
        user.set_password(password)
        user.is_sales = True
        user.save()
        
        # Handling many-to-many relationship
        
        return user
    
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from .models import Users
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse_lazy


from rest_framework_simplejwt.tokens import RefreshToken

class RegisterStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'address', 'password', 'password2', 'sales_person_id')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'], 
            address=validated_data['address'],  
            sales_person_id=validated_data['sales_person_id']    
        )
     
        user.set_password(validated_data['password'])
        user.is_student = True
        user.is_active = True  # Deactivate the user until they confirm registration
        user.save()

        return user
'''
        # Generate unique token for email confirmation
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        # Sending confirmation email with confirmation link
        subject = 'Registration Confirmation'
        confirmation_link = reverse_lazy('confirm-registration', kwargs={'uidb64': uid, 'token': token})
        confirmation_url = f'{settings.BASE_URL}{confirmation_link}'
        message = f'Dear {user.first_name} {user.last_name},\n\nThank you for registering to Universal Online University. \n\n You have already expressed interest in UOU, which means you aren not looking for an ordinary college experience. With academic centers around the Web, our network extends far beyond the vibrant community. We wish to foster an alumni who will serve the world more prestigious organizations. please view your site to obtain your course and grow as a person and gain we are pleased you have decided to join us.'
        from_email = 'universal.edu@example.com'  # Your email address
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Return tokens along with user data
        return {
            'refresh': str(refresh),
            'access': str(access),
            'user': user
        }

    @staticmethod
    def confirm_registration(uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = Users.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_email_confirmed = True
            user.is_active = True
            user.save()
            return user
        else:
            return None 
'''

class UsersSerializer(serializers.ModelSerializer):
    no_of_notifications = serializers.IntegerField()


    class Meta:
        model = Users 
        fields = ('first_name', 'last_name', 'email', 'phone', 'gender',
                  'emailfield', 'address', 'is_teacher', 'is_student',
                  'no_of_notifications')

    
    

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()

    def validate_email(self, value):
        # Check if the user exists with the provided email
        try:
            user = Users.objects.get(email=value)
        except Users.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class EmailSubscriptionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = EmailSubscription
        fields = ('__all__')

class CoursePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePurchaseRequest
        fields = ('_id', 'Instructor', 'title', 'language', 'content', 'courseduration', 'streamingtime', 'startingday', 'endingday', 'image', 'price', 'created_at')



class CouponPurchaseCouponSerializer(serializers.ModelSerializer):
    student_first_name = serializers.SerializerMethodField()
    student_last_name = serializers.SerializerMethodField()

    class Meta:
        model = CoursePurchaseCoupon
        fields = ('_id', 'coupon_code', 'student_id', 'course_id', 'student_first_name', 'student_last_name')

    def get_student_first_name(self, obj):
        try:
            student = Users.objects.get(id=obj.student_id)
            return student.first_name
        except Users.DoesNotExist:
            return None

    def get_student_last_name(self, obj):
        try:
            student = Users.objects.get(id=obj.student_id)
            return student.last_name
        except Users.DoesNotExist:
            return None


class LNMOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LNMOnline
        fields = ("id",)



class CouponPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponPurchase  # Define the model attribute correctly
        fields = '__all__'  # Use '__all__' to include all fields from the model
        
class PostSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Post
        fields = ('_id', 'video', 'image', 'caption', 'created_at')

import cloudinary.uploader
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books 
        fields =  ('__all__')



class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('_id', 'description', 'file', 'image', 'caption', 'audience', 'created_at')
        
     
class CourseSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Course
        fields =  ('__all__')


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

    

class StudentProfileSerializer(serializers.ModelSerializer):
    no_of_notifications = serializers.IntegerField()
    my_events = serializers.SerializerMethodField()
  
    class Meta:
        model = Users 
        fields =  ['id', 'first_name', 'last_name', 'email',
                   'phone', 'gender', 'emailfield', 'profile_imageId', 
                   'profile_imageUrl', 'background_imageId', 'background_imageUrl',
                   'address', 'Program', 'Term', 'my_courses',
                   'school_credentials_two_imageId', 'school_credentials_three_imageId',
                   'school_credentials_imageUrl', 'school_credentials_two_imageUrl', 
                   'school_credentials_three_imageUrl', 'no_of_notifications', 'my_events',
                  ]

    def get_my_events(self, obj):
        # Retrieve events associated with the user's courses
        my_courses = obj.my_courses
        if my_courses:
            return Events.objects.filter(audience=my_courses).values('id', 'title', 'startingtime', 'endtime', 'description', 'class_link', 'class_password',
                                                                      'startingday', 'endingday', 'audience', 'created_at').order_by('-created_at')
        else:
            return []  # Return an empty list if no courses are associated
        


class StudentEventSerializer(serializers.ModelSerializer):
    no_of_notifications = serializers.IntegerField()
    my_events = serializers.SerializerMethodField()
  
    class Meta:
        model = Users 
        fields =  ['id', 'no_of_notifications', 'my_events']

    def get_my_events(self, obj):
        # Retrieve events associated with the user's courses
        my_courses = obj.my_courses
        if my_courses:
            return Events.objects.filter(audience=my_courses).values('id', 'title', 'startingtime', 'endtime', 'description', 'class_link', 'class_password',
                                                                      'startingday', 'endingday', 'audience', 'created_at').order_by('-created_at')
        else:
            return []  # Return an empty list if no courses are associated


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users 
        fields =  ['id', 'profile_imageId', 'profile_imageUrl']


from django.conf import settings


class StudentCourseSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    class Meta:
        model = Users 
        fields = ['id', 'courses']
    def get_courses(self, obj):
        courses_data = []
        for course in obj.courses.all():
            course_data = {
                'id': course._id,
                'title': course.title,
                'Instructor': course.Instructor,
                'language': course.language,
                'content': course.content,
                'courseduration': course.courseduration,
                'streamingtime': course.streamingtime,
                'startingday': course.startingday,
                'endingday': course.endingday,
                'image': self.get_image_url(course.image, self.context['request']),
                'created_at': course.created_at
            }
            courses_data.append(course_data)
        return courses_data

    def get_image_url(self, image, request):
        if image:
            return request.build_absolute_uri(image.url)
        return None

