<?xml version='1.0' encoding='utf-8'?>
<scheme description="This pipeline predicts imagined motor actions using neural oscillatory pattern classification. The main node of this pipeline is the Common Spatial Pattern (CSP) filter, which is used to retrieve the components or patterns in the signal that are most suitable to represent desired categories or classes. CSP and its various extensions (available through NeuroPype) provide a powerful tool for building applications based on neural oscillations.&#10;This pipeline can be divided into 4 main parts, which we discuss in the following:&#10;&#10;Data acquisition:&#10;Includes : Import Data (here titled “Import SET”), LSL input/output, Stream Data and Inject Calibration Data nodes.&#10;In general you can process your data online or offline. For developing and testing purposes you will be mostly performing offline process using a pre-recorded file.&#10;&#10;- The “Import Data” nodes (here titled “Import Set”) are used to connect the pipeline to files.&#10;&#10;- The “LSL input” and “LSL output” nodes are used to get data stream into the pipeline, or send the data out to the network from the pipeline. (If you are sending markers make sure to check the “send marker” option in “LSL output” node)&#10;&#10;- The “Inject Calibration Data” node is used to pass the initial calibration data into the pipeline before the actual data is processed. The calibration data (Calib Data) is used by adaptive and machine learning algorithms to train and set their parameters initially. The main data is connected to the “Streaming Data” port.&#10;&#10;NOTE regarding “Inject Calibration Data”: &#10;In case you would like to train and test your pipeline using files (without using streaming node), you need to set the “Delay streaming packets” in this node. This enables the “Inject Calibration Data” node to buffer the test data that is pushed into it for one cycle and transfer it to the output port in the next cycle. It should be noted that the first cycle is used to push the calibration data through the pipeline.&#10;&#10;Data preprocess:&#10;Includes: Assign Targets, Select Range,  FIR filter and Segmentation nodes&#10;&#10;- The “Assign Target” node is mostly useful for the supervised learning algorithms, where  target values are assigned to specific markers present in the EEG signal. In order for this node to operate correctly you need to know the label for the markers in the data.&#10;&#10;- The “Select Range” node is used to specify certain parts of the data stream. For example, if we have a headset that contains certain bad channels, you can manually remove them here. That is the case for our example here where only data from the last 6 channels are used.&#10;&#10;- The “FIR Filter” node is used to remove the unwanted signals components outside of the EEG signal frequencies, e.g. to keep the 6-30 Hz frequency window.&#10;&#10;- The “Segmentation” node performs the epoching process, where the streamed data is divided into segments of the predefined window-length around the markers on the EEG data.&#10;&#10;NOTE regarding &quot;Segmentation&quot; node:&#10;The epoching process can be either done relative to the marker or the time window. When Processing a large file you should set the epoching relative to markers and while processing the streaming data, you should set it to sliding which chooses a single window at the end of the data.&#10;&#10;Feature extraction:&#10;&#10;Includes: Common Spatial Patterns (CSP) node&#10;As discussed above the spectral and spatial patterns in the data can be extracted by the CSP filters and its extensions.&#10;&#10;Classification:&#10;Includes: Variance, Logarithm, Logistic Regression and Measure Loss&#10;&#10;- The “Logistic Regression” node is used to perform the classification, where supervised learning methods is used to train the classifier. in this node you can choose the type of regularization and the regularization coefficient. You can also set the number of the folds for cross-validation in this node.&#10;&#10;- The “Measure Loss” node is used to measure various performance criteria. Here we use misclassification rate (MCR)." title="Simple Motor Imagery Prediction with CSP" version="2.0">
	<nodes>
		<node id="0" name="Assign Target Values" position="(500.0, 99.0)" project_name="NeuroPype" qualified_name="widgets.machine_learning.owassigntargets.OWAssignTargets" title="Assign Targets" uuid="a6316a51-0c78-4bdc-a363-9672f143c171" version="1.0.0" />
		<node id="1" name="Segmentation" position="(300, 300)" project_name="NeuroPype" qualified_name="widgets.formatting.owsegmentation.OWSegmentation" title="Segmentation" uuid="c8d8c21c-1535-4b71-b959-c4b159fb2902" version="1.0.1" />
		<node id="2" name="Measure Loss" position="(900, 400)" project_name="NeuroPype" qualified_name="widgets.machine_learning.owmeasureloss.OWMeasureLoss" title="Measure Loss" uuid="fad49ba9-accb-4a35-be3f-8c52ae4a3a06" version="1.0.2" />
		<node id="3" name="Common Spatial Patterns" position="(400, 300)" project_name="NeuroPype" qualified_name="widgets.neural.owcommonspatialpatterns.OWCommonSpatialPatterns" title="Common Spatial Patterns" uuid="017e7b5d-32d6-430b-9a68-1b364550491f" version="1.0.0" />
		<node id="4" name="Variance" position="(500, 300)" project_name="NeuroPype" qualified_name="widgets.statistics.owvariance.OWVariance" title="Variance" uuid="1dd0cd64-57ee-4624-96a6-166c69d7e5c1" version="1.0.0" />
		<node id="5" name="Logarithm" position="(600, 300)" project_name="NeuroPype" qualified_name="widgets.elementwise_math.owlogarithm.OWLogarithm" title="Logarithm" uuid="a52f60e6-1766-4b8f-b8d4-ac27770ce646" version="1.0.0" />
		<node id="6" name="Select Range" position="(600, 100)" project_name="NeuroPype" qualified_name="widgets.tensor_math.owselectrange.OWSelectRange" title="Select Range" uuid="915dcbda-58ff-4c60-ac0c-fabbff1223c6" version="1.0.0" />
		<node id="7" name="Logistic Regression" position="(700, 300)" project_name="NeuroPype" qualified_name="widgets.machine_learning.owlogisticregression.OWLogisticRegression" title="Logistic Regression" uuid="db367329-4fb3-47b1-86ff-dcd722e7b6e7" version="1.0.0" />
		<node id="8" name="FIR Filter" position="(200, 300)" project_name="NeuroPype" qualified_name="widgets.signal_processing.owfirfilter.OWFIRFilter" title="FIR Filter" uuid="2887e3ae-fbfc-4e8f-b0ca-47f82002dee6" version="1.0.0" />
		<node id="9" name="LSL Input" position="(100.0, 99.0)" project_name="NeuroPype" qualified_name="widgets.network.owlslinput.OWLSLInput" title="LSL Input" uuid="131ff9a0-be17-4c3f-980a-ead3cae01121" version="1.0.0" />
		<node id="10" name="Dejitter Timestamps" position="(200, 100)" project_name="NeuroPype" qualified_name="widgets.utilities.owdejittertimestamps.OWDejitterTimestamps" title="Dejitter Timestamps" uuid="f18e9e64-df45-41be-93a4-23eee9e90acf" version="1.0.0" />
		<node id="11" name="Inject Calibration Data" position="(400, 100)" project_name="NeuroPype" qualified_name="widgets.machine_learning.owinjectcalibrationdata.OWInjectCalibrationData" title="Inject Calibration Data" uuid="759eeae3-d643-4f1f-b766-391956e8f70f" version="1.0.0" />
		<node id="12" name="Override Axis" position="(796.0, 128.0)" project_name="NeuroPype" qualified_name="widgets.tensor_math.owoverrideaxis.OWOverrideAxis" title="Override Axis" uuid="4e1e72ae-22d9-4420-a373-49a748d3d60d" version="1.0.2" />
		<node id="13" name="Streaming Bar Plot" position="(938.0, 129.0)" project_name="NeuroPype" qualified_name="widgets.visualization.owbarplot.OWBarPlot" title="Streaming Bar Plot" uuid="6961bc5a-3668-4b9d-b757-84deb1355bac" version="1.0.2" />
		<node id="14" name="Print To Console" position="(832.0, 506.0)" project_name="NeuroPype" qualified_name="widgets.diagnostics.owprinttoconsole.OWPrintToConsole" title="Print To Console" uuid="a5c6777a-0184-4a8f-a506-2adb5f0568bd" version="1.0.0" />
		<node id="15" name="Streaming Bar Plot" position="(1158.0, 401.0)" project_name="NeuroPype" qualified_name="widgets.visualization.owbarplot.OWBarPlot" title="Streaming Bar Plot (1)" uuid="aa8bddce-dd55-472d-a019-713fa560322a" version="1.0.2" />
		<node id="16" name="Select Range" position="(1029.0, 400.0)" project_name="NeuroPype" qualified_name="widgets.tensor_math.owselectrange.OWSelectRange" title="Select Range" uuid="c1ce4faf-dc7a-4b3e-9e66-8941136ce90e" version="1.0.0" />
		<node id="17" name="Import XDF" position="(194.0, 5.0)" project_name="NeuroPype" qualified_name="widgets.file_system.owimportxdf.OWImportXDF" title="Import XDF" uuid="0ef887a2-069f-4fab-ab28-45c2402ffccf" version="1.0.0" />
		<node id="18" name="LSL Output" position="(1011.0, 276.0)" project_name="NeuroPype" qualified_name="widgets.network.owlsloutput.OWLSLOutput" title="LSL Output" uuid="c9278249-881d-4f34-a3db-e23555170ff8" version="1.0.0" />
	</nodes>
	<links>
		<link enabled="true" id="0" sink_channel="Data" sink_node_id="3" source_channel="Data" source_node_id="1" />
		<link enabled="true" id="1" sink_channel="Data" sink_node_id="4" source_channel="Data" source_node_id="3" />
		<link enabled="true" id="2" sink_channel="Data" sink_node_id="5" source_channel="Data" source_node_id="4" />
		<link enabled="true" id="3" sink_channel="Data" sink_node_id="6" source_channel="Data" source_node_id="0" />
		<link enabled="true" id="4" sink_channel="Data" sink_node_id="7" source_channel="Data" source_node_id="5" />
		<link enabled="true" id="5" sink_channel="Data" sink_node_id="2" source_channel="Data" source_node_id="7" />
		<link enabled="true" id="6" sink_channel="Data" sink_node_id="8" source_channel="Data" source_node_id="6" />
		<link enabled="true" id="7" sink_channel="Data" sink_node_id="1" source_channel="Data" source_node_id="8" />
		<link enabled="true" id="8" sink_channel="Data" sink_node_id="10" source_channel="Data" source_node_id="9" />
		<link enabled="true" id="9" sink_channel="Streaming Data" sink_node_id="11" source_channel="Data" source_node_id="10" />
		<link enabled="true" id="10" sink_channel="Data" sink_node_id="0" source_channel="Data" source_node_id="11" />
		<link enabled="true" id="11" sink_channel="Data" sink_node_id="12" source_channel="Data" source_node_id="7" />
		<link enabled="true" id="12" sink_channel="Data" sink_node_id="13" source_channel="Data" source_node_id="12" />
		<link enabled="true" id="13" sink_channel="Data" sink_node_id="15" source_channel="Data" source_node_id="16" />
		<link enabled="true" id="14" sink_channel="Data" sink_node_id="16" source_channel="Loss" source_node_id="2" />
		<link enabled="true" id="15" sink_channel="Data" sink_node_id="14" source_channel="Data" source_node_id="7" />
		<link enabled="true" id="16" sink_channel="Calib Data" sink_node_id="11" source_channel="Data" source_node_id="17" />
		<link enabled="true" id="17" sink_channel="Data" sink_node_id="18" source_channel="Data" source_node_id="7" />
	</links>
	<annotations />
	<thumbnail />
	<node_properties>
		<properties format="pickle" node_id="0">gAN9cQAoWBIAAABhbHNvX2xlZ2FjeV9vdXRwdXRxAYlYDgAAAGlzX2NhdGVnb3JpY2FscQKJWAkA
AABpdl9jb2x1bW5xA1gGAAAATWFya2VycQRYBwAAAG1hcHBpbmdxBX1xBihYBQAAAHJpZ2h0cQdL
AVgEAAAAbGVmdHEISwB1WA4AAABtYXBwaW5nX2Zvcm1hdHEJWAYAAABjb21wYXRxClgTAAAAc2F2
ZWRXaWRnZXRHZW9tZXRyeXELY3NpcApfdW5waWNrbGVfdHlwZQpxDFgMAAAAUHlRdDQuUXRDb3Jl
cQ1YCgAAAFFCeXRlQXJyYXlxDkMuAdnQywABAAAAAAAAAAACGgAAAXcAAAMhAAAACAAAAjkAAAFv
AAADGQAAAAAAAHEPhXEQh3ERUnESWA4AAABzZXRfYnJlYWtwb2ludHETiVgRAAAAc3VwcG9ydF93
aWxkY2FyZHNxFIlYCwAAAHVzZV9udW1iZXJzcRWJWAcAAAB2ZXJib3NlcRaJdS4=
</properties>
		<properties format="pickle" node_id="1">gAN9cQAoWBEAAABrZWVwX21hcmtlcl9jaHVua3EBiVgOAAAAbWF4X2dhcF9sZW5ndGhxAkc/yZmZ
mZmZmlgPAAAAb25saW5lX2Vwb2NoaW5ncQNYBwAAAHNsaWRpbmdxBFgNAAAAc2FtcGxlX29mZnNl
dHEFSwBYEwAAAHNhdmVkV2lkZ2V0R2VvbWV0cnlxBmNzaXAKX3VucGlja2xlX3R5cGUKcQdYDAAA
AFB5UXQ0LlF0Q29yZXEIWAoAAABRQnl0ZUFycmF5cQlDLgHZ0MsAAQAAAAAAAAAAAi8AAAF3AAAD
VAAAAAgAAAJOAAABbwAAA0wAAAAAAABxCoVxC4dxDFJxDVgOAAAAc2VsZWN0X21hcmtlcnNxDlgN
AAAAKHVzZSBkZWZhdWx0KXEPWA4AAABzZXRfYnJlYWtwb2ludHEQiVgLAAAAdGltZV9ib3VuZHNx
EUc/4AAAAAAAAEdADAAAAAAAAIZxElgHAAAAdmVyYm9zZXETiXUu
</properties>
		<properties format="pickle" node_id="2">gAN9cQAoWBIAAABhY2N1bXVsYXRlX29mZmxpbmVxAYlYCgAAAGNvbmRfZmllbGRxAlgLAAAAVGFy
Z2V0VmFsdWVxA1gNAAAAaWdub3JlX3Jlc2V0c3EEiVgLAAAAbG9zc19tZXRyaWNxBVgDAAAATUNS
cQZYFgAAAG91dHB1dF9mb3Jfc3RhdHNfdGFibGVxB4lYEwAAAHNhdmVkV2lkZ2V0R2VvbWV0cnlx
CGNzaXAKX3VucGlja2xlX3R5cGUKcQlYDAAAAFB5UXQ0LlF0Q29yZXEKWAoAAABRQnl0ZUFycmF5
cQtDLgHZ0MsAAQAA///7hAAAAc////z7AAACwf//+4wAAAHu///88wAAArkAAAABAABxDIVxDYdx
DlJxD1gOAAAAc2V0X2JyZWFrcG9pbnRxEIl1Lg==
</properties>
		<properties format="pickle" node_id="3">gAN9cQAoWAoAAABjb25kX2ZpZWxkcQFYCwAAAFRhcmdldFZhbHVlcQJYDwAAAGluaXRpYWxpemVf
b25jZXEDiVgDAAAAbm9mcQRLAlgTAAAAc2F2ZWRXaWRnZXRHZW9tZXRyeXEFY3NpcApfdW5waWNr
bGVfdHlwZQpxBlgMAAAAUHlRdDQuUXRDb3JlcQdYCgAAAFFCeXRlQXJyYXlxCEMuAdnQywABAAAA
AAMEAAABmAAABHsAAAJgAAADDAAAAbcAAARzAAACWAAAAAAAAHEJhXEKh3ELUnEMWA4AAABzZXRf
YnJlYWtwb2ludHENiXUu
</properties>
		<properties format="pickle" node_id="4">gAN9cQAoWAQAAABheGlzcQFYBAAAAHRpbWVxAlgSAAAAZGVncmVlc19vZl9mcmVlZG9tcQNLAFgS
AAAAZm9yY2VfZmVhdHVyZV9heGlzcQSJWBMAAABzYXZlZFdpZGdldEdlb21ldHJ5cQVjc2lwCl91
bnBpY2tsZV90eXBlCnEGWAwAAABQeVF0NC5RdENvcmVxB1gKAAAAUUJ5dGVBcnJheXEIQy4B2dDL
AAEAAAAABEQAAAJXAAAFuwAAAwoAAARMAAACdgAABbMAAAMCAAAAAQAAcQmFcQqHcQtScQxYDgAA
AHNldF9icmVha3BvaW50cQ2JdS4=
</properties>
		<properties format="literal" node_id="5">{'base': '(use default)', 'savedWidgetGeometry': None, 'set_breakpoint': False}</properties>
		<properties format="pickle" node_id="6">gAN9cQAoWBMAAABhcHBseV9tdWx0aXBsZV9heGVzcQGJWAQAAABheGlzcQJYBQAAAHNwYWNlcQNY
EwAAAHNhdmVkV2lkZ2V0R2VvbWV0cnlxBGNzaXAKX3VucGlja2xlX3R5cGUKcQVYDAAAAFB5UXQ0
LlF0Q29yZXEGWAoAAABRQnl0ZUFycmF5cQdDLgHZ0MsAAQAAAAADDAAAAasAAASDAAACiwAAAxQA
AAHKAAAEewAAAoMAAAAAAABxCIVxCYdxClJxC1gJAAAAc2VsZWN0aW9ucQxYAwAAADotNnENWA4A
AABzZXRfYnJlYWtwb2ludHEOiVgEAAAAdW5pdHEPWAcAAABpbmRpY2VzcRB1Lg==
</properties>
		<properties format="literal" node_id="7">{'alphas': [0.1, 0.5, 1.0, 5, 10.0], 'bias_scaling': 1.0, 'class_weights': 'auto', 'cond_field': 'TargetValue', 'dont_reset_model': False, 'dual_formulation': False, 'include_bias': True, 'initialize_once': True, 'max_iter': 100, 'multiclass': 'ovr', 'num_folds': 5, 'num_jobs': 1, 'probabilistic': True, 'regularizer': 'l2', 'savedWidgetGeometry': None, 'search_metric': 'accuracy', 'set_breakpoint': False, 'solver': 'lbfgs', 'tolerance': 0.0001, 'verbosity': 0}</properties>
		<properties format="pickle" node_id="8">gAN9cQAoWA0AAABhbnRpc3ltbWV0cmljcQGJWAQAAABheGlzcQJYBAAAAHRpbWVxA1gSAAAAY29u
dm9sdXRpb25fbWV0aG9kcQRYCAAAAHN0YW5kYXJkcQVYDgAAAGN1dF9wcmVyaW5naW5ncQaJWAsA
AABmcmVxdWVuY2llc3EHXXEIKEsGSwdLHksgZVgNAAAAbWluaW11bV9waGFzZXEJiFgEAAAAbW9k
ZXEKWAgAAABiYW5kcGFzc3ELWAUAAABvcmRlcnEMWA0AAAAodXNlIGRlZmF1bHQpcQ1YEwAAAHNh
dmVkV2lkZ2V0R2VvbWV0cnlxDmNzaXAKX3VucGlja2xlX3R5cGUKcQ9YDAAAAFB5UXQ0LlF0Q29y
ZXEQWAoAAABRQnl0ZUFycmF5cRFDLgHZ0MsAAQAAAAADDAAAAXIAAASDAAACxAAAAxQAAAGRAAAE
ewAAArwAAAAAAABxEoVxE4dxFFJxFVgOAAAAc2V0X2JyZWFrcG9pbnRxFolYCgAAAHN0b3BfYXR0
ZW5xF0dASQAAAAAAAHUu
</properties>
		<properties format="pickle" node_id="9">gAN9cQAoWA0AAABjaGFubmVsX25hbWVzcQFdcQJYCwAAAGRpYWdub3N0aWNzcQOJWAwAAABtYXJr
ZXJfcXVlcnlxBFgAAAAAcQVYDAAAAG1heF9ibG9ja2xlbnEGTQAEWAoAAABtYXhfYnVmbGVucQdL
HlgMAAAAbWF4X2NodW5rbGVucQhLAFgMAAAAbm9taW5hbF9yYXRlcQlYDQAAACh1c2UgZGVmYXVs
dClxClgFAAAAcXVlcnlxC1gQAAAAbmFtZT0nb2JjaV9lZWcyJ3EMWAcAAAByZWNvdmVycQ2IWBQA
AAByZXNvbHZlX21pbmltdW1fdGltZXEORz/gAAAAAAAAWBMAAABzYXZlZFdpZGdldEdlb21ldHJ5
cQ9jc2lwCl91bnBpY2tsZV90eXBlCnEQWAwAAABQeVF0NC5RdENvcmVxEVgKAAAAUUJ5dGVBcnJh
eXESQy4B2dDLAAEAAAAAATQAAAEkAAACqwAAApEAAAE8AAABQwAAAqMAAAKJAAAAAAAAcROFcRSH
cRVScRZYDgAAAHNldF9icmVha3BvaW50cReJdS4=
</properties>
		<properties format="pickle" node_id="10">gAN9cQAoWA8AAABmb3JjZV9tb25vdG9uaWNxAYhYDwAAAGZvcmdldF9oYWxmdGltZXECTSwBWA4A
AABtYXhfdXBkYXRlcmF0ZXEDTfQBWBMAAABzYXZlZFdpZGdldEdlb21ldHJ5cQRjc2lwCl91bnBp
Y2tsZV90eXBlCnEFWAwAAABQeVF0NC5RdENvcmVxBlgKAAAAUUJ5dGVBcnJheXEHQy4B2dDLAAEA
AAAABEgAAAI/AAAFtwAAAxkAAARMAAACVgAABbMAAAMVAAAAAAAAcQiFcQmHcQpScQtYDgAAAHNl
dF9icmVha3BvaW50cQyJWA4AAAB3YXJtdXBfc2FtcGxlc3ENSv////91Lg==
</properties>
		<properties format="literal" node_id="11">{'delay_streaming_packets': False, 'savedWidgetGeometry': None, 'set_breakpoint': False}</properties>
		<properties format="pickle" node_id="12">gAN9cQAoWA8AAABheGlzX29jY3VycmVuY2VxAUsAWBAAAABjYXJyeV9vdmVyX25hbWVzcQKIWBIA
AABjYXJyeV9vdmVyX251bWJlcnNxA4hYDAAAAGN1c3RvbV9sYWJlbHEEWA0AAAAodXNlIGRlZmF1
bHQpcQVYCQAAAGluaXRfZGF0YXEGXXEHKFgEAAAAbGVmdHEIWAUAAAByaWdodHEJZVgIAAAAbmV3
X2F4aXNxClgHAAAAZmVhdHVyZXELWAgAAABvbGRfYXhpc3EMWAcAAABmZWF0dXJlcQ1YDAAAAG9u
bHlfc2lnbmFsc3EOiVgTAAAAc2F2ZWRXaWRnZXRHZW9tZXRyeXEPY3NpcApfdW5waWNrbGVfdHlw
ZQpxEFgMAAAAUHlRdDQuUXRDb3JlcRFYCgAAAFFCeXRlQXJyYXlxEkMuAdnQywABAAAAAAMEAAAB
XwAABHsAAAKZAAADDAAAAX4AAARzAAACkQAAAAAAAHEThXEUh3EVUnEWWA4AAABzZXRfYnJlYWtw
b2ludHEXiXUu
</properties>
		<properties format="pickle" node_id="13">gAN9cQAoWA0AAABhbHdheXNfb25fdG9wcQGJWAQAAABheGlzcQJYBwAAAGZlYXR1cmVxA1gQAAAA
YmFja2dyb3VuZF9jb2xvcnEEWAcAAAAjRkZGRkZGcQVYCQAAAGJhcl9jb2xvcnEGWAEAAABicQdY
CQAAAGJhcl93aWR0aHEIRz/szMzMzMzNWAwAAABpbml0aWFsX2RpbXNxCV1xCihLMksyTbwCTfQB
ZVgOAAAAaW5zdGFuY2VfZmllbGRxC1gNAAAAKHVzZSBkZWZhdWx0KXEMWA4AAABsYWJlbF9yb3Rh
dGlvbnENWAoAAABob3Jpem9udGFscQ5YEwAAAHNhdmVkV2lkZ2V0R2VvbWV0cnlxD2NzaXAKX3Vu
cGlja2xlX3R5cGUKcRBYDAAAAFB5UXQ0LlF0Q29yZXERWAoAAABRQnl0ZUFycmF5cRJDLgHZ0MsA
AQAAAAADBAAAAUQAAAR7AAADCwAAAwwAAAFjAAAEcwAAAwMAAAAAAABxE4VxFIdxFVJxFlgOAAAA
c2V0X2JyZWFrcG9pbnRxF4lYDAAAAHNob3dfdG9vbGJhcnEYiVgLAAAAc3RyZWFtX25hbWVxGVgN
AAAAKHVzZSBkZWZhdWx0KXEaWAUAAAB0aXRsZXEbWA4AAABDbGFzc2lmaWNhdGlvbnEcWBEAAAB1
c2VfbGFzdF9pbnN0YW5jZXEdiFgHAAAAdmVyYm9zZXEeiVgIAAAAeV9saW1pdHNxH11xIChLAEsB
ZXUu
</properties>
		<properties format="literal" node_id="14">{'only_nonempty': True, 'print_channel': False, 'print_compact': True, 'print_data': False, 'print_markers': False, 'print_streams': [], 'print_time': False, 'print_trial': False, 'savedWidgetGeometry': None, 'set_breakpoint': False}</properties>
		<properties format="pickle" node_id="15">gAN9cQAoWA0AAABhbHdheXNfb25fdG9wcQGJWAQAAABheGlzcQJYBwAAAGZlYXR1cmVxA1gQAAAA
YmFja2dyb3VuZF9jb2xvcnEEWAcAAAAjRkZGRkZGcQVYCQAAAGJhcl9jb2xvcnEGWAEAAABycQdY
CQAAAGJhcl93aWR0aHEIRz/VHrhR64UfWAwAAABpbml0aWFsX2RpbXNxCV1xCihNIANLMk0sAU30
AWVYDgAAAGluc3RhbmNlX2ZpZWxkcQtYDQAAACh1c2UgZGVmYXVsdClxDFgOAAAAbGFiZWxfcm90
YXRpb25xDVgKAAAAaG9yaXpvbnRhbHEOWBMAAABzYXZlZFdpZGdldEdlb21ldHJ5cQ9jc2lwCl91
bnBpY2tsZV90eXBlCnEQWAwAAABQeVF0NC5RdENvcmVxEVgKAAAAUUJ5dGVBcnJheXESQy4B2dDL
AAEAAP//+4QAAAFl///8+wAAAyz///uMAAABhP///PMAAAMkAAAAAQAAcROFcRSHcRVScRZYDgAA
AHNldF9icmVha3BvaW50cReJWAwAAABzaG93X3Rvb2xiYXJxGIlYCwAAAHN0cmVhbV9uYW1lcRlo
DFgFAAAAdGl0bGVxGlgWAAAATWlzY2xhc3NpZmljYXRpb24gUmF0ZXEbWBEAAAB1c2VfbGFzdF9p
bnN0YW5jZXEciFgHAAAAdmVyYm9zZXEdiVgIAAAAeV9saW1pdHNxHl1xHyhLAEsBZXUu
</properties>
		<properties format="pickle" node_id="16">gAN9cQAoWBMAAABhcHBseV9tdWx0aXBsZV9heGVzcQGJWAQAAABheGlzcQJYBwAAAGZlYXR1cmVx
A1gTAAAAc2F2ZWRXaWRnZXRHZW9tZXRyeXEEY3NpcApfdW5waWNrbGVfdHlwZQpxBVgMAAAAUHlR
dDQuUXRDb3JlcQZYCgAAAFFCeXRlQXJyYXlxB0MuAdnQywABAAD///uEAAAB2P///PsAAAK4///7
jAAAAff///zzAAACsAAAAAEAAHEIhXEJh3EKUnELWAkAAABzZWxlY3Rpb25xDF1xDVgDAAAATUNS
cQ5hWA4AAABzZXRfYnJlYWtwb2ludHEPiVgEAAAAdW5pdHEQWAUAAABuYW1lc3ERdS4=
</properties>
		<properties format="pickle" node_id="17">gAN9cQAoWA0AAABjbG91ZF9hY2NvdW50cQFYAAAAAHECWAwAAABjbG91ZF9idWNrZXRxA2gCWBEA
AABjbG91ZF9jcmVkZW50aWFsc3EEaAJYCgAAAGNsb3VkX2hvc3RxBVgHAAAARGVmYXVsdHEGWAgA
AABmaWxlbmFtZXEHWCIAAABDOi9EYXRhc2V0cy9BZGFtL21pX2NhbGliX2FkYW0ueGRmcQhYEwAA
AGhhbmRsZV9jbG9ja19yZXNldHNxCYhYEQAAAGhhbmRsZV9jbG9ja19zeW5jcQqIWBUAAABoYW5k
bGVfaml0dGVyX3JlbW92YWxxC4hYDgAAAG1heF9tYXJrZXJfbGVucQxYDQAAACh1c2UgZGVmYXVs
dClxDVgSAAAAcmVvcmRlcl90aW1lc3RhbXBzcQ6JWA4AAAByZXRhaW5fc3RyZWFtc3EPaA1YEwAA
AHNhdmVkV2lkZ2V0R2VvbWV0cnlxEGNzaXAKX3VucGlja2xlX3R5cGUKcRFYDAAAAFB5UXQ0LlF0
Q29yZXESWAoAAABRQnl0ZUFycmF5cRNDLgHZ0MsAAQAAAAADBAAAASgAAAR7AAAC0QAAAwwAAAFH
AAAEcwAAAskAAAAAAABxFIVxFYdxFlJxF1gOAAAAc2V0X2JyZWFrcG9pbnRxGIlYDwAAAHVzZV9z
dHJlYW1uYW1lc3EZiVgHAAAAdmVyYm9zZXEaiXUu
</properties>
		<properties format="pickle" node_id="18">gAN9cQAoWAkAAABjaHVua19sZW5xAUsAWBUAAABpZ25vcmVfc2lnbmFsX2NoYW5nZWRxAolYCwAA
AG1hcmtlcl9uYW1lcQNYEQAAAE91dFN0cmVhbS1tYXJrZXJzcQRYEAAAAG1hcmtlcl9zb3VyY2Vf
aWRxBVgAAAAAcQZYDAAAAG1heF9idWZmZXJlZHEHSzxYFwAAAHJlc2V0X2lmX2xhYmVsc19jaGFu
Z2VkcQiJWBMAAABzYXZlZFdpZGdldEdlb21ldHJ5cQljc2lwCl91bnBpY2tsZV90eXBlCnEKWAwA
AABQeVF0NC5RdENvcmVxC1gKAAAAUUJ5dGVBcnJheXEMQy4B2dDLAAEAAAAAAwQAAAEmAAAEewAA
AtIAAAMMAAABRQAABHMAAALKAAAAAAAAcQ2FcQ6HcQ9ScRBYDAAAAHNlbmRfbWFya2Vyc3ERiVgO
AAAAc2V0X2JyZWFrcG9pbnRxEolYCQAAAHNvdXJjZV9pZHETaAZYBQAAAHNyYXRlcRRYDQAAACh1
c2UgZGVmYXVsdClxFVgLAAAAc3RyZWFtX25hbWVxFlgGAAAAbWlfbHNscRdYCwAAAHN0cmVhbV90
eXBlcRhYAgAAAE1JcRlYEwAAAHVzZV9kYXRhX3RpbWVzdGFtcHNxGohYFgAAAHVzZV9udW1weV9v
cHRpbWl6YXRpb25xG4l1Lg==
</properties>
	</node_properties>
	<patch>{
    "description": {
        "description": "(description missing)",
        "license": "",
        "name": "(untitled)",
        "status": "(unspecified)",
        "url": "",
        "version": "0.0.0"
    },
    "edges": [
        [
            "node2",
            "data",
            "node4",
            "data"
        ],
        [
            "node4",
            "data",
            "node5",
            "data"
        ],
        [
            "node5",
            "data",
            "node6",
            "data"
        ],
        [
            "node1",
            "data",
            "node7",
            "data"
        ],
        [
            "node6",
            "data",
            "node8",
            "data"
        ],
        [
            "node8",
            "data",
            "node3",
            "data"
        ],
        [
            "node8",
            "data",
            "node13",
            "data"
        ],
        [
            "node8",
            "data",
            "node15",
            "data"
        ],
        [
            "node8",
            "data",
            "node19",
            "data"
        ],
        [
            "node7",
            "data",
            "node9",
            "data"
        ],
        [
            "node9",
            "data",
            "node2",
            "data"
        ],
        [
            "node10",
            "data",
            "node11",
            "data"
        ],
        [
            "node11",
            "data",
            "node12",
            "streaming_data"
        ],
        [
            "node12",
            "data",
            "node1",
            "data"
        ],
        [
            "node13",
            "data",
            "node14",
            "data"
        ],
        [
            "node17",
            "data",
            "node16",
            "data"
        ],
        [
            "node3",
            "loss",
            "node17",
            "data"
        ],
        [
            "node18",
            "data",
            "node12",
            "calib_data"
        ]
    ],
    "nodes": {
        "node1": {
            "class": "AssignTargets",
            "module": "neuropype.nodes.machine_learning.AssignTargets",
            "params": {
                "also_legacy_output": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "is_categorical": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "iv_column": {
                    "customized": false,
                    "type": "StringPort",
                    "value": "Marker"
                },
                "mapping": {
                    "customized": true,
                    "type": "Port",
                    "value": {
                        "left": 0,
                        "right": 1
                    }
                },
                "mapping_format": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "compat"
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "support_wildcards": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "use_numbers": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "verbose": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "a6316a51-0c78-4bdc-a363-9672f143c171"
        },
        "node10": {
            "class": "LSLInput",
            "module": "neuropype.nodes.network.LSLInput",
            "params": {
                "channel_names": {
                    "customized": false,
                    "type": "ListPort",
                    "value": []
                },
                "diagnostics": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "marker_query": {
                    "customized": false,
                    "type": "StringPort",
                    "value": ""
                },
                "max_blocklen": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 1024
                },
                "max_buflen": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 30
                },
                "max_chunklen": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 0
                },
                "nominal_rate": {
                    "customized": false,
                    "type": "FloatPort",
                    "value": null
                },
                "query": {
                    "customized": true,
                    "type": "StringPort",
                    "value": "name='obci_eeg2'"
                },
                "recover": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "resolve_minimum_time": {
                    "customized": false,
                    "type": "FloatPort",
                    "value": 0.5
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "131ff9a0-be17-4c3f-980a-ead3cae01121"
        },
        "node11": {
            "class": "DejitterTimestamps",
            "module": "neuropype.nodes.utilities.DejitterTimestamps",
            "params": {
                "force_monotonic": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "forget_halftime": {
                    "customized": true,
                    "type": "FloatPort",
                    "value": 300
                },
                "max_updaterate": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 500
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "warmup_samples": {
                    "customized": false,
                    "type": "IntPort",
                    "value": -1
                }
            },
            "uuid": "f18e9e64-df45-41be-93a4-23eee9e90acf"
        },
        "node12": {
            "class": "InjectCalibrationData",
            "module": "neuropype.nodes.machine_learning.InjectCalibrationData",
            "params": {
                "delay_streaming_packets": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "759eeae3-d643-4f1f-b766-391956e8f70f"
        },
        "node13": {
            "class": "OverrideAxis",
            "module": "neuropype.nodes.tensor_math.OverrideAxis",
            "params": {
                "axis_occurrence": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 0
                },
                "carry_over_names": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "carry_over_numbers": {
                    "customized": true,
                    "type": "BoolPort",
                    "value": true
                },
                "custom_label": {
                    "customized": false,
                    "type": "StringPort",
                    "value": null
                },
                "init_data": {
                    "customized": true,
                    "type": "ListPort",
                    "value": [
                        "left",
                        "right"
                    ]
                },
                "new_axis": {
                    "customized": true,
                    "type": "EnumPort",
                    "value": "feature"
                },
                "old_axis": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "feature"
                },
                "only_signals": {
                    "customized": true,
                    "type": "BoolPort",
                    "value": false
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "4e1e72ae-22d9-4420-a373-49a748d3d60d"
        },
        "node14": {
            "class": "BarPlot",
            "module": "neuropype.nodes.visualization.BarPlot",
            "params": {
                "always_on_top": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "axis": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "feature"
                },
                "background_color": {
                    "customized": false,
                    "type": "StringPort",
                    "value": "#FFFFFF"
                },
                "bar_color": {
                    "customized": false,
                    "type": "StringPort",
                    "value": "b"
                },
                "bar_width": {
                    "customized": true,
                    "type": "FloatPort",
                    "value": 0.9
                },
                "initial_dims": {
                    "customized": false,
                    "type": "ListPort",
                    "value": [
                        50,
                        50,
                        700,
                        500
                    ]
                },
                "instance_field": {
                    "customized": false,
                    "type": "StringPort",
                    "value": null
                },
                "label_rotation": {
                    "customized": true,
                    "type": "EnumPort",
                    "value": "horizontal"
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "show_toolbar": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "stream_name": {
                    "customized": false,
                    "type": "StringPort",
                    "value": null
                },
                "title": {
                    "customized": true,
                    "type": "StringPort",
                    "value": "Classification"
                },
                "use_last_instance": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "verbose": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "y_limits": {
                    "customized": true,
                    "type": "ListPort",
                    "value": [
                        0,
                        1
                    ]
                }
            },
            "uuid": "6961bc5a-3668-4b9d-b757-84deb1355bac"
        },
        "node15": {
            "class": "PrintToConsole",
            "module": "neuropype.nodes.diagnostics.PrintToConsole",
            "params": {
                "only_nonempty": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "print_channel": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "print_compact": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "print_data": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "print_markers": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "print_streams": {
                    "customized": false,
                    "type": "ListPort",
                    "value": []
                },
                "print_time": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "print_trial": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "a5c6777a-0184-4a8f-a506-2adb5f0568bd"
        },
        "node16": {
            "class": "BarPlot",
            "module": "neuropype.nodes.visualization.BarPlot",
            "params": {
                "always_on_top": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "axis": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "feature"
                },
                "background_color": {
                    "customized": false,
                    "type": "StringPort",
                    "value": "#FFFFFF"
                },
                "bar_color": {
                    "customized": true,
                    "type": "StringPort",
                    "value": "r"
                },
                "bar_width": {
                    "customized": false,
                    "type": "FloatPort",
                    "value": 0.33
                },
                "initial_dims": {
                    "customized": true,
                    "type": "ListPort",
                    "value": [
                        800,
                        50,
                        300,
                        500
                    ]
                },
                "instance_field": {
                    "customized": false,
                    "type": "StringPort",
                    "value": null
                },
                "label_rotation": {
                    "customized": true,
                    "type": "EnumPort",
                    "value": "horizontal"
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "show_toolbar": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "stream_name": {
                    "customized": false,
                    "type": "StringPort",
                    "value": null
                },
                "title": {
                    "customized": true,
                    "type": "StringPort",
                    "value": "Misclassification Rate"
                },
                "use_last_instance": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "verbose": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "y_limits": {
                    "customized": true,
                    "type": "ListPort",
                    "value": [
                        0,
                        1
                    ]
                }
            },
            "uuid": "aa8bddce-dd55-472d-a019-713fa560322a"
        },
        "node17": {
            "class": "SelectRange",
            "module": "neuropype.nodes.tensor_math.SelectRange",
            "params": {
                "apply_multiple_axes": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "axis": {
                    "customized": true,
                    "type": "EnumPort",
                    "value": "feature"
                },
                "selection": {
                    "customized": true,
                    "type": "Port",
                    "value": [
                        "MCR"
                    ]
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "unit": {
                    "customized": true,
                    "type": "EnumPort",
                    "value": "names"
                }
            },
            "uuid": "c1ce4faf-dc7a-4b3e-9e66-8941136ce90e"
        },
        "node18": {
            "class": "ImportXDF",
            "module": "neuropype.nodes.file_system.ImportXDF",
            "params": {
                "cloud_account": {
                    "customized": false,
                    "type": "StringPort",
                    "value": ""
                },
                "cloud_bucket": {
                    "customized": false,
                    "type": "StringPort",
                    "value": ""
                },
                "cloud_credentials": {
                    "customized": false,
                    "type": "StringPort",
                    "value": ""
                },
                "cloud_host": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "Default"
                },
                "filename": {
                    "customized": true,
                    "type": "StringPort",
                    "value": "C:/Datasets/Adam/mi_calib_adam.xdf"
                },
                "handle_clock_resets": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "handle_clock_sync": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "handle_jitter_removal": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "max_marker_len": {
                    "customized": false,
                    "type": "IntPort",
                    "value": null
                },
                "reorder_timestamps": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "retain_streams": {
                    "customized": false,
                    "type": "Port",
                    "value": null
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "use_streamnames": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "verbose": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "0ef887a2-069f-4fab-ab28-45c2402ffccf"
        },
        "node19": {
            "class": "LSLOutput",
            "module": "neuropype.nodes.network.LSLOutput",
            "params": {
                "chunk_len": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 0
                },
                "ignore_signal_changed": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "marker_name": {
                    "customized": false,
                    "type": "StringPort",
                    "value": "OutStream-markers"
                },
                "marker_source_id": {
                    "customized": false,
                    "type": "StringPort",
                    "value": ""
                },
                "max_buffered": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 60
                },
                "reset_if_labels_changed": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "send_markers": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "source_id": {
                    "customized": false,
                    "type": "StringPort",
                    "value": ""
                },
                "srate": {
                    "customized": false,
                    "type": "FloatPort",
                    "value": null
                },
                "stream_name": {
                    "customized": true,
                    "type": "StringPort",
                    "value": "mi_lsl"
                },
                "stream_type": {
                    "customized": true,
                    "type": "StringPort",
                    "value": "MI"
                },
                "use_data_timestamps": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "use_numpy_optimization": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "c9278249-881d-4f34-a3db-e23555170ff8"
        },
        "node2": {
            "class": "Segmentation",
            "module": "neuropype.nodes.formatting.Segmentation",
            "params": {
                "keep_marker_chunk": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "max_gap_length": {
                    "customized": false,
                    "type": "FloatPort",
                    "value": 0.2
                },
                "online_epoching": {
                    "customized": true,
                    "type": "EnumPort",
                    "value": "sliding"
                },
                "sample_offset": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 0
                },
                "select_markers": {
                    "customized": false,
                    "type": "ListPort",
                    "value": null
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "time_bounds": {
                    "customized": true,
                    "type": "ListPort",
                    "value": [
                        0.5,
                        3.5
                    ]
                },
                "verbose": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "c8d8c21c-1535-4b71-b959-c4b159fb2902"
        },
        "node3": {
            "class": "MeasureLoss",
            "module": "neuropype.nodes.machine_learning.MeasureLoss",
            "params": {
                "accumulate_offline": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "cond_field": {
                    "customized": false,
                    "type": "StringPort",
                    "value": "TargetValue"
                },
                "ignore_resets": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "loss_metric": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "MCR"
                },
                "output_for_stats_table": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "fad49ba9-accb-4a35-be3f-8c52ae4a3a06"
        },
        "node4": {
            "class": "CommonSpatialPatterns",
            "module": "neuropype.nodes.neural.CommonSpatialPatterns",
            "params": {
                "cond_field": {
                    "customized": false,
                    "type": "StringPort",
                    "value": "TargetValue"
                },
                "initialize_once": {
                    "customized": true,
                    "type": "BoolPort",
                    "value": false
                },
                "nof": {
                    "customized": true,
                    "type": "IntPort",
                    "value": 2
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "017e7b5d-32d6-430b-9a68-1b364550491f"
        },
        "node5": {
            "class": "Variance",
            "module": "neuropype.nodes.statistics.Variance",
            "params": {
                "axis": {
                    "customized": true,
                    "type": "EnumPort",
                    "value": "time"
                },
                "degrees_of_freedom": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 0
                },
                "force_feature_axis": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "1dd0cd64-57ee-4624-96a6-166c69d7e5c1"
        },
        "node6": {
            "class": "Logarithm",
            "module": "neuropype.nodes.elementwise_math.Logarithm",
            "params": {
                "base": {
                    "customized": false,
                    "type": "FloatPort",
                    "value": null
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                }
            },
            "uuid": "a52f60e6-1766-4b8f-b8d4-ac27770ce646"
        },
        "node7": {
            "class": "SelectRange",
            "module": "neuropype.nodes.tensor_math.SelectRange",
            "params": {
                "apply_multiple_axes": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "axis": {
                    "customized": true,
                    "type": "EnumPort",
                    "value": "space"
                },
                "selection": {
                    "customized": true,
                    "type": "Port",
                    "value": ":-6"
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "unit": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "indices"
                }
            },
            "uuid": "915dcbda-58ff-4c60-ac0c-fabbff1223c6"
        },
        "node8": {
            "class": "LogisticRegression",
            "module": "neuropype.nodes.machine_learning.LogisticRegression",
            "params": {
                "alphas": {
                    "customized": false,
                    "type": "ListPort",
                    "value": [
                        0.1,
                        0.5,
                        1.0,
                        5,
                        10.0
                    ]
                },
                "bias_scaling": {
                    "customized": false,
                    "type": "FloatPort",
                    "value": 1.0
                },
                "class_weights": {
                    "customized": true,
                    "type": "Port",
                    "value": "auto"
                },
                "cond_field": {
                    "customized": false,
                    "type": "StringPort",
                    "value": "TargetValue"
                },
                "dont_reset_model": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "dual_formulation": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "include_bias": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "initialize_once": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "max_iter": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 100
                },
                "multiclass": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "ovr"
                },
                "num_folds": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 5
                },
                "num_jobs": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 1
                },
                "probabilistic": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "regularizer": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "l2"
                },
                "search_metric": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "accuracy"
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "solver": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "lbfgs"
                },
                "tolerance": {
                    "customized": false,
                    "type": "FloatPort",
                    "value": 0.0001
                },
                "verbosity": {
                    "customized": false,
                    "type": "IntPort",
                    "value": 0
                }
            },
            "uuid": "db367329-4fb3-47b1-86ff-dcd722e7b6e7"
        },
        "node9": {
            "class": "FIRFilter",
            "module": "neuropype.nodes.signal_processing.FIRFilter",
            "params": {
                "antisymmetric": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "axis": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "time"
                },
                "convolution_method": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "standard"
                },
                "cut_preringing": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "frequencies": {
                    "customized": true,
                    "type": "ListPort",
                    "value": [
                        6,
                        7,
                        30,
                        32
                    ]
                },
                "minimum_phase": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": true
                },
                "mode": {
                    "customized": false,
                    "type": "EnumPort",
                    "value": "bandpass"
                },
                "order": {
                    "customized": false,
                    "type": "IntPort",
                    "value": null
                },
                "set_breakpoint": {
                    "customized": false,
                    "type": "BoolPort",
                    "value": false
                },
                "stop_atten": {
                    "customized": false,
                    "type": "FloatPort",
                    "value": 50.0
                }
            },
            "uuid": "2887e3ae-fbfc-4e8f-b0ca-47f82002dee6"
        }
    },
    "version": 1.1
}</patch>
</scheme>
