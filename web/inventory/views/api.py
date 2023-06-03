from django.db.models import QuerySet
from rest_framework import viewsets, permissions, generics, response, mixins, status
from inventory.models import System
from inventory.models.motherboard import Motherboard

from inventory.serializers import SystemSerializer


class SystemApiViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet):
    """SystemApiViewSet
    This API is provided to for each agent.
    The agent will be able to add its information to central server through this api.
    The only permission is reserved for each node is the create permission.
    If "node" attribute in System object is already added or already exists in the database,
    the agent's information will be updated in database.
    """
    queryset = System.objects.all().order_by('node')
    serializer_class = SystemSerializer
    permission_classes = [permissions.DjangoModelPermissions, permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        TODO: [HIGH] the old information of that agent should be marked as is_active, like:
         - NetworkInterface
         - IPV4
         - Printer
         - PrinterDriver
         - InstalledSoftware
         - User
        """
        print('*' * 100, self.request.data)
        try:
            dic_motherboard = self.request.data.pop('motherboard')
            if System.objects.filter(node=request.data['node']).exists():
                print('EXISTS')
                instance = System.objects.get(node=request.data['node'])
                serializer = self.get_serializer(instance, data=request.data, partial=None)
                serializer.is_valid(raise_exception=True)
                motherboard_instance = instance.motherboard
                motherboard_instance.manufacturer = dic_motherboard['manufacturer']
                motherboard_instance.product = dic_motherboard['product']
                motherboard_instance.version = dic_motherboard['version']
                motherboard_instance.save()
                serializer.save(motherboard=motherboard_instance)
                if getattr(instance, '_prefetched_objects_cache', None):
                    instance._prefetched_objects_cache = {}
                return response.Response(serializer.data)
            else:
                print('NOT EXISTS')
                serializer = self.get_serializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                print('is_valid')
                motherboard_instance = Motherboard(
                    manufacturer=dic_motherboard['manufacturer'],
                    product=dic_motherboard['product'],
                    version=dic_motherboard['version']
                )
                motherboard_instance.save()
                print(motherboard_instance.pk)
                serializer.save(motherboard=motherboard_instance)
                print('serializer.save')
                headers = self.get_success_headers(serializer.data)
                return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as x:
            print(str(x))
