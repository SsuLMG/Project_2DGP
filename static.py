
class Define:
    instance = None
    def __init__(self):
        if Define.instance is None:
            Define.instance = self
        self.score = 0