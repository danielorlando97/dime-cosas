class TelegramGroupMessageInfo:
    def __init__(self, text, sender, date, group, dialog_id, sms_url) -> None:
        self.text = text
        self.sender = sender
        self.date = date
        self.group = group
        self.dialog_id = dialog_id
        self.sms_url = sms_url

# TODO: Save User Photo
class TelegramUserInfo:
    def __init__(self, name, username, phone, photo = None) -> None:
        self.name = name
        self.username = username
        self.phone = phone
        self.photo = photo