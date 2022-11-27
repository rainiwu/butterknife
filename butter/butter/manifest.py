class Manifest:
    def __init__(
        self,
        totalChunks: int = 0,
        framePerChunks: int = 0,
        frameRate: int = 0,
        buff: int = 0,
    ):
        self.totalChunks = totalChunks
        self.framePerChunk = framePerChunks
        self.frameRate = frameRate
        # 0 for unbuffered, 1 for buffered
        self.buff = buff
