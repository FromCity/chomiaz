from rest_framework import viewsets
from rest_framework.response import Response
import json
from .forms import DataForm
from .models import Message
from django.http import HttpResponse, HttpResponseNotFound
from .serializers import MessageForUserSerializer, MessageDetailSerializer
from .tasks import process_message


class BotViewSet(viewsets.ViewSet):
    """
    """

    def create(self, request):
        request_body_bytes = request.body.decode('utf-8')
        data = json.loads(request_body_bytes)
        form = DataForm(data)
        if form.is_valid():
            external_message_id = data['external_message_id']
            if Message.objects.filter(
                external_message_id=external_message_id).exists():
                message = Message.objects.get(external_message_id=external_message_id)
                id = message.id
                status = message.status
                data = {'id':id, 'status': status, 'duplicate': True}
                return Response(data = data, status=403)
            Message.objects.create(**data)
            message = Message.objects.get(external_message_id=data['external_message_id'])
            process_message.apply_async(args=[external_message_id])
            return Response(data = {"id": message.id, "status": message.status}, status=201)
        else:
            err_mes = str()
            for field, errors in form.errors.items():
                for error in errors:
                    # Обработка отдельной ошибки
                    err_mes += f"Ошибка в поле {field}: {error}"
            return Response(data=err_mes, status=400)

    def destroy(self, request, pk=None):
        response = Message.objects.get(external_message_id=pk).delete()
        return HttpResponse([response])

def Messages(request, user_id):
    if Message.objects.filter(user_id=user_id).exists():
        queryset = Message.objects.filter(user_id=user_id).order_by("created_at")
        serializer = MessageForUserSerializer(queryset, many=True)
        response = serializer.data
        return HttpResponse([response])
    else:
        return HttpResponse('Сообщения не найдены')


def MessageDetail(request, id):
    if Message.objects.filter(id=id).exists():
        queryset = Message.objects.get(id=id)
        serializer = MessageDetailSerializer(queryset)
        response = serializer.data
        return HttpResponse([response])
    else:
        return HttpResponseNotFound('Сообщение не найдено')