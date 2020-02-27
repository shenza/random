from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from api_test.apps.bankai.serializers import ControlSerializer
from api_test.apps.bankai.renderers import  ControlCSVRenderer
from api_test.apps.bankai.models import Control
from rest_framework.settings import api_settings
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer
from django.urls  import reverse
from datetime import datetime

#    curl -X "DELETE" http://127.0.0.1:8000/api2/control/66/
#    curl -X PUT -H "Content-Type: application/json" -d '{"data":{"id":65, "type":"Control", "attributes": { "name": "ichigo", "type": "Primitive",  "maximum_rabi_rate": "64",  "polar_angle": "0.27"   }	} }' http://127.0.0.1:8000/api2/control/66/

class ControlViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Control.objects.all()
    serializer_class = ControlSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                          #IsOwnerOrReadOnly]
    parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (CSVRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def perform_create(self, serializer):
        serializer.save()
        #serializer.save(owner=self.request.user) 


    @action(detail=False, methods=['get'], renderer_classes=[ControlCSVRenderer] + api_settings.DEFAULT_RENDERER_CLASSES)
    def download(self, request):
        """
        Export all controls in CSV format.

        The CSV header is in order of: name, type, maximum_rabi_rate,
        polar_angle
        """
        csv_req = self.request.query_params.get('format', '')
        content = [{
            'name': control.name,
            'type': control.type,
            'maximum_rabi_rate': control.maximum_rabi_rate,
            'polar_angle': control.polar_angle
        } for control in self.queryset]
        if csv_req.lower()=="csv":
            filename = {'Content-Disposition':'attachment; filename=controls_%s.csv' % datetime.now()}
            return Response(content, headers=filename)
        return Response(content)

    
    @action(methods=['POST'], detail=False)
    def bulk_upload(self, request, *args, **kwargs):
        """
        Bulk upload controls in CSV format.

        curl -X POST -H 'Content-Type: text/csv' -H 'Accept: text/csv' --data-binary @control_uploads.csv http://127.0.0.1:8000/api2/control/bulk_upload/
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers={'Location': reverse('control-list')})
