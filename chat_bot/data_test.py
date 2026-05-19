payload = {
  "external_message_id": "msg-test",
  "user_id": "user-42",
  "text": "Хочу узнать статус заказа 12345",
  "created_at": "2026-05-13T10:00:00Z"
}

payload_order_status = {
  "external_message_id": "msg-test1",
  "user_id": "user-42",
  "text": "Хочу проверить заказ 12345",
  "created_at": "2026-05-13T10:00:00Z"
}

payload_operator_request ={
  "external_message_id": "msg-test2",
  "user_id": "user-42",
  "text": "Хочу услышать оператора operator",
  "created_at": "2026-05-13T10:00:00Z"
}

payload_unknown = {
  "external_message_id": "msg-test3",
  "user_id": "user-42",
  "text": "Подскажите где вы находитесь",
  "created_at": "2026-05-13T10:00:00Z"
}

payload_history1 = {
  "external_message_id": "msg-test4",
  "user_id": "user-42",
  "text": "Подскажите где вы находитесь",
  "created_at": "2026-05-13T10:00:00Z"
}

payload_history2 = {
  "external_message_id": "msg-test5",
  "user_id": "user-42",
  "text": "Хочу услышать оператора operator",
  "created_at": "2026-05-13T10:00:00Z"
}

data_history = [{
  "external_message_id": "msg-test4",
  "user_id": "user-42",
  "text": "Подскажите где вы находитесь",
  "created_at": "2026-05-13T10:00:00Z"
},{
  "external_message_id": "msg-test5",
  "user_id": "user-42",
  "text": "Хочу услышать оператора operator",
  "created_at": "2026-05-13T10:00:00Z"
}
]