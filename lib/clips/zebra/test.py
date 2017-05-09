import clips
clips.BatchStar("zebra.clp")
clips.Reset()
clips.Run()
s = clips.StdoutStream.Read()

print s
