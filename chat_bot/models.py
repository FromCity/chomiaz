from django.db import models


    # --- Статусы обработки ---
class Status(models.TextChoices):
    RECEIVED ="received", "Принято"
    PROCESSING ="processing", "В обработке"
    PROCESSED = "processed", "Обработано"
    FAILED = "failed", "Ошибка"


    # --- Типы сообщений после обработки ---
class MessageType(models.TextChoices):
    ORDER_STATUS = 'order_status', 'Текст содержит слово «заказ» или «order»'
    OPERATOR_REQUEST = 'operator_request', 'Текст содержит «оператор», «менеджер» или «operator»'
    UNKNOWN = 'unknown', 'Остальные сообщения'

# Create your models here.
class Message(models.Model):
    id = models.AutoField(verbose_name="Внутренний идентификатор сообщения", primary_key=True)
    external_message_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='ID сообщения во внешней системе',
        help_text='Должен быть уникальным',
    )
    user_id = models.CharField(
        max_length=255,
        verbose_name='ID пользователя во внешней системе',
    )
    text = models.TextField(
        verbose_name='Текст сообщения',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RECEIVED,
        verbose_name='Статус обработки',
        db_index=True,
    )

    message_type = models.CharField(
        max_length=20,
        choices=MessageType.choices,
        default=MessageType.UNKNOWN,
        verbose_name='Тип сообщения после обработки',
    )

    response_text = models.TextField(
        verbose_name='Ответ пользователю',
    )

    error_text = models.TextField(
        verbose_name='Текст ошибки',
        blank=True,
        default='',
        help_text='Заполняется, если обработка завершилась неуспешно',
    )

    created_at = models.DateTimeField(
        verbose_name='Дата создания сообщения во внешней системе',
    )

    received_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата получения webhook сервисом',
    )

    processed_at = models.DateTimeField(
        null=True,
        verbose_name='Дата завершения обработки',
    )