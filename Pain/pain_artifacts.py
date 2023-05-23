import json
import os

pain_artifacts = [
    {
        "artifact_name" : "Alpha Decrease Frontal",
        "band_ranges" : [(8, 13)],
        "channels" : [ 0, 1],
        "effect" : -1,
        "delay" : 0.3,
        "duration" : 1
    },
    {
        "artifact_name" : "Beta Increase Posterior",
        "band_ranges" : [(20,25)],
        "channels" : [ 5,6,7,13,14,15],
        "effect" : 1,
        "delay" : 0.3,
        "duration" : 1
    },
]

            
def ParseArtifact(index):#more easily read an artifact
    artifact        = pain_artifacts[index]
    name            = artifact["artifact_name"]
    band_ranges     = artifact["band_ranges"]
    channels        = artifact["channels"]
    effect          = artifact["effect"]
    delay           = artifact["delay"]
    duration        = artifact["duration"]
    #print(f"Artiface : {name}")
    #print(f"Band ramges : {band_ranges}")
    #print(f"Channels : {channels}")
    #print(f"Effect : {effect}")
    return name, band_ranges, channels, effect, delay, duration
