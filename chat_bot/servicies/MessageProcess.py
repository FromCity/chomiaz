from datetime import datetime, timezone
from chat_bot.models import Message
from chat_bot.models import Status
from chat_bot.models import MessageType


def get_message_type(text):
    message_type = str()
    if "заказ" in text or "order" in text:
        message_type = MessageType.ORDER_STATUS
    elif "оператор" in text or "менеджер" in text or "operator" in text:
        message_type = MessageType.OPERATOR_REQUEST
    else:
        message_type = MessageType.UNKNOWN
    return message_type


def get_response_text(message_type):
    response_text = str()
    if message_type == MessageType.ORDER_STATUS:
        response_text = "Ваш запрос по заказу принят в обработку"
    elif message_type == MessageType.OPERATOR_REQUEST:
        response_text = "Передаю ваш запрос оператору"
    elif message_type == MessageType.UNKNOWN:
        response_text = "Повторите запрос"
    return response_text


def process(external_message_id):
    message = Message.objects.get(external_message_id=external_message_id)
    message.status = Status.PROCESSING
    message.save()
    text = message.text
    text = text.lower()
    message_type = get_message_type(text=text)
    response_text = get_response_text(message_type=message_type)
    message.status = Status.PROCESSED
    message.message_type = message_type
    message.response_text = response_text
    message.processed_at = datetime.now(timezone.utc)
    message.save()
    return True


if __name__ == '__main__':
    text = "Хочу проверить заказ 12345"

    def get_message_type(text):
        message_type = str()
        if "заказ" in text or "order" in text:
            message_type = "order"
        elif "оператор" in text or "менеджер" in text or "operator":
            message_type = "operator"
        else:
            message_type = 'unknown'
        print('message_type', message_type)
    get_message_type(text)
