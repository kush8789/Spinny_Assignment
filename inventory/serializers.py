from rest_framework import serializers
from .models import Box
from django.utils import timezone
from store.settings import A1, V1, L1, L2
from datetime import date, timedelta
from django.db.models import Sum

class BoxSerializer(serializers.ModelSerializer):
    area = serializers.SerializerMethodField()
    volume = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height', 'area', 'volume', 'creator', 'created_at', 'updated_at']
        read_only_fields = ['creator', 'created_at', 'updated_at']

    def get_area(self, obj):
        return obj.area

    def get_volume(self, obj):
        return obj.volume

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime('%Y-%m-%d %H:%M:%S')

    def get_updated_at(self, obj):
        return timezone.localtime(obj.updated_at).strftime('%Y-%m-%d %H:%M:%S')

    def validate(self, attrs):
        total_area = Box.objects.aggregate(total_area=Sum('area'))['total_area'] or 0
        total_volume = Box.objects.filter(creator=self.context['request'].user).aggregate(total_volume=Sum('volume'))['total_volume'] or 0
        existing_count = Box.objects.count()
        
        new_area = attrs['length'] * attrs["breadth"]
        new_volume = new_area * attrs["height"]

        if (total_area + new_area) / (existing_count + 1) > A1:
            raise serializers.ValidationError("Max Area Limit will exceed")

        if (total_volume + new_volume) / (existing_count + 1) > V1:
            raise serializers.ValidationError("Max Volume Limit will exceed")

        week_count = Box.objects.filter(created_at__gte=date.today() - timedelta(days=7)).count()
        if week_count >= L1:
            raise serializers.ValidationError("Max weekly count Limit will exceed")

        week_count_user = Box.objects.filter(created_at__gte=date.today() - timedelta(days=7), creator=self.context['request'].user).count()
        if week_count_user >= L2:
            raise serializers.ValidationError("Your Max weekly count Limit will exceed")

        return attrs
    
    def update(self, instance, validated_data):
        instance.length = validated_data.get('length', instance.length)
        instance.breadth = validated_data.get('breadth', instance.breadth)
        instance.height = validated_data.get('height', instance.height)

        # Recalculate area and volume
        instance.area = instance.calculate_area()
        instance.volume = instance.calculate_volume()

        instance.save()
        return instance