from dataclasses import dataclass


@dataclass
class TextButton:
    count_price = "Рассчитать стоимости"
    send_price = 'Разослать стоимости'
    send_confirm = 'Разослать подтверждение курса/клуба'
    send_simple_message = 'Отправить простое сообщение всем'
    send_by_sheet = 'Рассылка по листу'

