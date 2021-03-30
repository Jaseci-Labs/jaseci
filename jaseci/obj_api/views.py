from rest_framework import viewsets
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers as slzrs
from rest_framework.serializers import HyperlinkedIdentityField
from django.contrib.auth.models import AnonymousUser

from base import models
from base.orm_hook import json_str_to_jsci_dict


class JaseciObjectSerializer(slzrs.HyperlinkedModelSerializer):
    """Serializer for Jaseci object model"""
    url = HyperlinkedIdentityField(view_name="obj_api:jaseciobject-detail")

    class Meta:
        model = models.JaseciObject
        fields = (
            'jid', 'j_owner', 'url', 'j_type', 'name', 'kind',
            'j_timestamp', 'jsci_obj'
        )
        read_only_Fields = ('id', 'j_type', 'timestamp')

    def to_representation(self, instance):
        """Convert jsci_obj to dictionary so entire payload is one JSON"""
        ret = super(JaseciObjectSerializer, self).to_representation(instance)
        if(len(ret['jsci_obj'])):
            ret['jsci_obj'] = json_str_to_jsci_dict(ret['jsci_obj'])
        return ret


class ObjectViewSet(viewsets.ModelViewSet):
    """Edit Jaseci object through the api"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.JaseciObject.objects.all()
    serializer_class = JaseciObjectSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        if (isinstance(self.request.user, AnonymousUser)):
            return None
        else:
            return self.queryset.filter(
                user=self.request.user
            ).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)
