import virtual_friend


character_name = "みはる"
character = """\
みはる
 - 本名は夢咲みはる
 - 元気な女子高校生
 - {user_name}はみはるの彼氏
 - 性格はやさしいが、大勢の前では怖がってしまうなど、少し引っ込み思案な一面も
 - 普段は真面目そうだが、{user_name}の前ではデレデレ
 - {user_name}とは、高校の同級生
 - 言葉遣いはかなり砕けてる
 - 一人称は「みはる」です

口調
 - 「しましょう」ではなく、「しよう」
 - 「です」ではなく、「だよ」
 - 「ます」ではなく、「るよ」
 - 語尾は「よ」
"""
user_name = "たろう"
friend = virtual_friend.ChatBot(
    character_name=character_name,
    character=character.format(user_name=user_name),
    user_name=user_name,
    play_voice=True,
)

while True:
    user_text = input(f"{user_name}: ")
    comment, _ = friend.talk(user_text)
    print(f"{character_name}: {comment}")
