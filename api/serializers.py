from rest_framework import serializers


from dashboard.master.models import UserDetail, User
from home.models import BookCallBack

from dashboard.services.models import (
    StichingCategory,
    StichingService,
    StichingFinish,
    StichingPattern
)

SignUpUser = User
SignUpDetail = UserDetail
BookCallBack = BookCallBack 
StichingCategory = StichingCategory
StichingFinish = StichingFinish
StichingService = StichingService
StichingPattern = StichingPattern


class BookCallBackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookCallBack
        fields = ('id', 'mobile_no', 'note', 'created_at', 'updated_at')


class SignUpSerializer(serializers.ModelSerializer):
    # first_name = serializers.SerializerMethodField('get_first_name')
    # last_name = serializers.SerializerMethodField('get_last_name')
    # email = serializers.SerializerMethodField('get_email')
    # role = serializers.SerializerMethodField('get_role')

    # def get_first_name(self, obj):
    #     return obj.user.first_name

    # def get_last_name(self, obj):
    #     return obj.user.last_name
    
    # def get_email(self, obj):
    #     return obj.user.email
    
    # def get_role(self, obj):
    #     return obj.user.role

    class Meta:
        model = SignUpDetail
        fields = (
            'user_id',            
            'mobile_no',            
            'address',
            'land_mark',
            'location',
            'pincode',
            'address_type'
        )

class StichingCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StichingCategory 
        fields = (
            'id',
            'name'
        )