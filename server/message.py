import os

class MessageIDs:
    SUBSCRIBE = 200
    VOICE_DUMP = 201
    BANK_DUMP = 202
    VOICE_LOAD = 203        # {category, bankName, voiceIndex}
    BANK_UPLOAD = 204       # {category, bankName}

    NEW_USER_BANK = 210     # {bankName}
    DELETE_USER_BANK = 211  # {bankIndex}
    BANK_UPLOAD = 212       # {bankName, data}

    VOICE_INIT = 220        # {}
    VOICE_NAME = 221        # {voiceName}
    VOICE_STORE = 222       # {voiceIndex(0-31)}

    GET_SETTINGS = 230
    SET_SETTINGS = 231

    ERROR_MESSAGE = 666


class Message(list):
    def __init__(self, data: list) -> None:
        super().__init__(data)
        assert len(self) == 2
    
    @staticmethod
    def id():
        raise NotImplementedError()
    
    @staticmethod
    def getId(data: list):
        assert len(data) > 0, f"Invalid message: {data}"
        assert type(data[0]) is int, f'Invalid message: {data}'
        return int(data[0])

class SubscribeMessage:
    @staticmethod
    def id():
        return MessageIDs.SUBSCRIBE


class VoiceLoadMessage(Message):
    @staticmethod
    def id():
        return MessageIDs.VOICE_LOAD
    
    def category(self) -> str:
        return str(self[1][0])
    
    def bankIndex(self) -> int:
        return int(self[1][1])
    
    def voiceIndex(self) -> int:
        return int(self[1][2])
    
class VoiceStoreMessage(Message):
    @staticmethod
    def id():
        return MessageIDs.VOICE_STORE
    
    def category(self) -> str:
        return str(self[1][0])
    
    def bankIndex(self) -> int:
        return int(self[1][1])
    
    def voiceIndex(self) -> int:
        return int(self[1][2])
    
class VoiceNameMessage(Message):
    @staticmethod
    def id():
        return MessageIDs.VOICE_NAME
    
    def voiceName(self) -> str:
        assert type(self[1]) is str, f'Expected string name, got {self[1]} ({type(self[1])})'
        return self[1][:10]

class NewUserBankMessage(Message):
    @staticmethod
    def id():
        return MessageIDs.NEW_USER_BANK
    
    def bankName(self):
        assert len(self) == 2, f'Incomplete new user bank message: {self}'
        assert type(self[1]) is str, f'Expected string name, got {self[1]} ({type(self[1])})'
        return self[1]
    

class DeleteUserBankMessage(Message):
    @staticmethod
    def id():
        return MessageIDs.DELETE_USER_BANK
    
    def bankIndex(self) -> int:
        return int(self[1][1])
    
    def bankCategory(self) -> str:
        return str(self[1][0])

class GetSettingsMessage(Message):
    @staticmethod
    def id():
        return MessageIDs.GET_SETTINGS
    

class SetSettingsMessage(Message):
    @staticmethod
    def id():
        return MessageIDs.SET_SETTINGS
