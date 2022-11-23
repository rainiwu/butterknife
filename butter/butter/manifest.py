class manifest(object):
    def __init__(self, totalChunks=0, framePerChunks=0, frameRate=0):
        self.totalChunks = totalChunks
        self.framePerChunk = framePerChunks
        self.frameRate = frameRate