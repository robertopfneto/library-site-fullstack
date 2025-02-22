from rest_framework import serializers
from .models import Categoria, Leitura, Livro, Trofeu, User
from django.contrib.auth import authenticate


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class TrofeuSerializer(serializers.ModelSerializer):
    categorias = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Trofeu
        fields = '__all__'
        extra_kwargs = {
            'categoria': {'write_only': True}
        }

class UserSerializer(serializers.ModelSerializer):
    trofeus = TrofeuSerializer(many=True, read_only=True) 

    class Meta:
        model = User
        fields = '__all__'


class LivroSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)
    class Meta:
        model = Livro
        fields = '__all__'

class LeituraSerializer(serializers.ModelSerializer):
    livros = LivroSerializer(many=True, read_only=True)  
    class Meta:
        model = Leitura
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciais inválidas")