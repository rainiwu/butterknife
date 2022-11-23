class manifest:
    def __init__(self, totalChunks=0, framePerChunks=0, frameRate=0, buff=0):
        self.totalChunks = totalChunks
        self.framePerChunk = framePerChunks
        self.frameRate = frameRate
        #0 for unbuffered, 1 for buffered
        self.buff = buff