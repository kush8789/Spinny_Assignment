from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Box
from .serializers import BoxSerializer
from .filters import BoxFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user

class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoxFilter

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied('Only staff can add boxes.')
        
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if not self.request.user.is_staff:
            raise PermissionDenied('Only staff can update boxes.')

        validated_data = serializer.validated_data
        if 'creator' in validated_data or 'created_at' in validated_data:
            raise PermissionDenied('Cannot change creator or creation date.')

        serializer.save()
        
    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied('Only the creator can delete this box.')
        instance.delete()

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'retrieve':
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'my_boxes':
            self.permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]
        else:
            self.permission_classes = [IsStaffOrReadOnly]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsStaffOrReadOnly])
    def my_boxes(self, request):
        boxes = Box.objects.filter(creator=request.user)
        serializer = self.get_serializer(boxes, many=True)
        return Response(serializer.data)
