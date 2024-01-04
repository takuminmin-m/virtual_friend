class Conversation():

    def __init__(self, num_keep_histories: int) -> None:
        self.histories = []
        self.num_keep_histories = num_keep_histories

    def add(self, speaker_name: str, text: str):
        self.histories.append({
            "speaker_name": speaker_name,
            "text": text,
        })

        while len(self.histories) > self.num_keep_histories:
            self.histories.pop(0)

    def all_histories(self):
        return self.histories

    def to_string(self):
        messages = map(lambda m:f"{m['speaker_name']}「{m['text']}」", self.histories)
        return "\n".join(messages)
