from rest_framework import serializers
from .models import Categoria, Conquista, Leitura, Livro, TrofeuConfig, User
from django.contrib.auth import authenticate

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class TrofeuConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrofeuConfig
        fields = '__all__'

class ConquistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conquista
        fields = '__all__'
        extra_kwargs = {
            'trofeu_config': {'required': True}  
        }

class UserSerializer(serializers.ModelSerializer):
    conquistas = ConquistaSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'
        extra_kwargs = {
            'categoria': {'required': False}
        }

class LeituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leitura
        fields = '__all__'
        read_only_fields = ('data_leitura',)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciais inválidas")