from rest_framework import serializers
from florence.models import Intlib, Import, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nick', 'avatar']
        read_only_fields = fields


# class ImportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Import
#         fields = ['alias', 'lib']
#         read_only_fields = fields


class IntlibSearchSerializer(serializers.ModelSerializer):
# class IntlibSerializer(serializers.HyperlinkedModelSerializer):
    # author = UserSerializer()
    author_avatar = serializers.CharField(source='author.avatar', read_only=True)

    class Meta:
        model = Intlib
        fields = ['id', 'name', 'author_avatar', 'description', 'version']
        read_only_fields = fields
