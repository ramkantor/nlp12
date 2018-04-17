import re
class segmentTag:
    def __init__(self, str):
        segmentTag = re.split(r'\t', str)

        self.segment = segmentTag[0]
        self.tag = segmentTag[1].strip()