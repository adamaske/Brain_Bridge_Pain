import json
import os

pain_artifacts = [
    {
        "artifact_name" : "EXAMPLE",
        "band_ranges" : [(8, 13), (30, 40)],
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

name, band_ranges, affected_channels, effect = ParseArtifact(0)#parse the artifact
for band_range in band_ranges:
    start_frequency = band_range[0]
    end_frequency = band_range[1]
    print(f"Start : {start_frequency}")
    print(f"End : {end_frequency}")