import json
import os

pain_artifacts = [
    {
        "artifact_name" : "Decrease in Alpha over PreFrontal cortex",
        "band_ranges" : [(8, 13)],
        "channels" : [ 0,1],
        "effect" : 1,
        "delay" : 0.2,
        "duration" : 1
    },
    {
        "artifact_name" : "Decrease Beta",
        "band_ranges" : [(13,32)],
        "channels" : [ 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
        "effect" : -1,
        "delay" : 0.2,
        "duration" : 1
    },
    {
        "artifact_name" : "Overreations in high theta and low beta ",
        "band_ranges" : [(6,9), (12,16)],
        "channels" : [ 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
        "effect" : 1,
        "delay" : 0.2,
        "duration" : 0.5
    },
    {
        "artifact_name" : "Decrease theta and gamme over frontal areas",
        "band_ranges" : [(4,8), (30,60)],
        "channels" : [ 0,1,2,3,4,5,6],
        "effect" : 1,
        "delay" : 0.2,
        "duration" : 0.5
    },
    {
        "artifact_name" : "Decrease alpha beta theta over midline electrodes",
        "band_ranges" : [(8,13), (13,30), (5,9)],
        "channels" : [ 7,8,8,9,10,11,12],
        "effect" : 1,
        "delay" : 0.2,
        "duration" : 0.5
    }
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
