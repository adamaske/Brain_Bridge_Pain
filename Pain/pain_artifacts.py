import json
import os

pain_artifacts = [
    {
        "artifact_name" : "EXAMPLE",
        "band_ranges" : [(8, 13), (20, 28)],
        "channels" : [ 0, 1, 2],
        "effect" : 1,
        "delay" : 0,
        "duration" : 1
    },
]

            
def ParseArtifact(index):#more easily read an artifact
    artifact        = pain_artifacts[index]
    name            = artifact["artifact_name"]
    band_ranges     = artifact["band_ranges"]
    channels        = artifact["channels"]
    effect          = artifact["effect"]
    
    #print(f"Artiface : {name}")
    #print(f"Band ramges : {band_ranges}")
    #print(f"Channels : {channels}")
    #print(f"Effect : {effect}")
    return name, band_ranges, channels, effect
