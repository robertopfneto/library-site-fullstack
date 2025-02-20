from rest_framework import serializers
from .models import Leitura, Livro, Trofeu, User

class TrofeuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trofeu
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    trofeus = TrofeuSerializer(many=True, read_only=True) 

    class Meta:
        model = User
        fields = '__all__'


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'

class LeituraSerializer(serializers.ModelSerializer):
    livros = LivroSerializer(many=True, read_only=True)  
    class Meta:
        model = Leitura
        fields = '__all__'