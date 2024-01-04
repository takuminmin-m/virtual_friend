import requests, simpleaudio, tempfile, json


class VoicevoxAPI():

    def __init__(
        self,
        speaker_id:int = 10,
        host:str = "127.0.0.1",
        port = 50021,
    ):
        self.speaker_id = speaker_id
        self.host = host
        self.port = port

    def _url(self, params):
        return f"http://{self.host}:{self.port}/{params}"

    def _generate_audio_query(self, params):
        response = requests.post(
            self._url("audio_query"),
            params=params,
        )
        audio_query = response.json()

        return audio_query

    def _generate_synthesis(self, params, audio_query):
        response = requests.post(
            self._url("synthesis"),
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(audio_query),
        )
        return response.content

    def generate_voice(self, text, play_voice=True):
        params = (
            ("text", text),
            ("speaker", self.speaker_id),
        )
        audio_query = self._generate_audio_query(params)
        voice_wave_bytes = self._generate_synthesis(params, audio_query)
        self._play_voice(voice_wave_bytes)

        return voice_wave_bytes

    def _play_voice(self, voice_data_bytes):

        with tempfile.TemporaryDirectory() as tmp:
            file_path = f"{tmp}/generated_voice.wav"

            with open(file_path, "wb") as f:
                f.write(voice_data_bytes)
                wave_obj = simpleaudio.WaveObject.from_wave_file(file_path)
                play_obj = wave_obj.play()
                play_obj.wait_done()
