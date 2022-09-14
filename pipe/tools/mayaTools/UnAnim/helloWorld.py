class words:
    def __init__(self):
        self.hello = "hello"
        self.space = " "
        self.world = "world"

wordList = []
for var in vars(words):
    wordList.append(getattr(words, var))

print(wordList)
