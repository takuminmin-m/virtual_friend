from .conversation import Conversation
from .language_model import LanguageModel
from .text_to_speech import VoicevoxAPI

import textwrap, re


class ChatBot():

    def __init__(
        self,
        character_name:str,
        character:str,
        user_name:str,
        play_voice = True,
    ) -> None:
        self.lm = LanguageModel(cuda_device_id=1)
        self.conversation = Conversation(10)
        self.text_to_speech = VoicevoxAPI()

        prompt_templete = """\
            ユーザー: 以下のキャラクター設定に基づき、{character_name}の次のセリフを書いてください
            {character}

            {character_name}と{user_name}は学校の帰り道で会話しています
            {context}

            システム: {character_name}「"""
        # """  """内のインデントを除去
        self.prompt_templete = textwrap.dedent(prompt_templete)
        self.character_name = character_name
        self.character = character
        self.user_name = user_name

        self.play_voice = True

    def _prompt(self):
        params = {
            "character_name": self.character_name,
            "character": self.character,
            "user_name": self.user_name,
            "context": self.conversation.to_string(),
        }
        return self.prompt_templete.format(**params)

    def _split_generated_text(self, output:str):
        pattern = f"システム: {self.character_name}「(.*)」"
        return re.findall(pattern, output)[0]

    def talk(self, text:str):
        self.conversation.add(self.user_name, text)
        output = self.lm(self._prompt())
        generated_comment = self._split_generated_text(output)

        self.conversation.add(self.character_name, generated_comment)

        voice_data_bytes = self.text_to_speech.generate_voice(
            generated_comment,
            play_voice = self.play_voice,
        )

        return generated_comment, voice_data_bytes
