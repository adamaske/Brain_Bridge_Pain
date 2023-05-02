from pylsl import resolve_stream
from pylsl import StreamInlet



if __name__ == "__main__":
  print("Waiting for Motor Imagery stream!")
  streams = resolve_stream('name', 'mi_lsl')
  #we're only sending eeg data at this time so we grab that
  #we can send everything over this same stream, then just grab other elements from the stream
  inlet  = StreamInlet(streams[0])
  while True:
    sample = inlet.pull_sample()
    print(f"Left : {sample[0][0]:.1f} || Right : {sample[0][1]:.1f}")