import pain_artifacts
all_artifacts = pain_artifacts.pain_artifacts
for artifact in range(len(all_artifacts)):
    obj = all_artifacts[artifact]
    name = obj["artifact_name"]
    band_range = obj["band_range"]
    channels = obj["channels"]

    print(f"Artiface : {name}")
    print(f"Band ramge : {band_range}")
    print(f"Channels : {channels}")