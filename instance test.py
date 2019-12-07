class speaker:
    def __init__(self, word):
        self.word = word
    
    def speak(self):
        print(self.word)

    def set_word(self, word):
        self.word = word


class containter:
    def __init__(self, speaker):
        self.speaker = speaker


my_speaker = speaker("hello")
containter_a = containter(my_speaker)
containter_b = containter(my_speaker)

containter_b.speaker.set_word("good bye")

containter_a.speaker.speak()
containter_b.speaker.speak()




