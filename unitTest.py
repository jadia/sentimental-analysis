import time


class TweepyUnitTest:
    def __init__(self, keyword):
        self.keyword = keyword

    def analyse(self):
        time.sleep(5)
        return 'Analysis Result for %s' % self.keyword
