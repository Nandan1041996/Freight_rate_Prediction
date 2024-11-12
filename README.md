--> Objective is to Calculate the Freight Rate For New Year 

--> User First calculate Calculate Inc/Dec Rate and then Proposed Freight Costs Calculation

--> First Calculate Percentage Increase/decrease and pass this parameter to Proposed Freight Costs Calculation for calculate new freight rate.

--> Input Parameters : 
	1) Calculate Inc/Dec Rate contains two params 
		1)New Diesel Rate/Liter (Based On Veraval) 
		2)Old Diesel Rate/Liter (Based On Veraval)
	2) Proposed Freight Costs Calculation contains params
		1) Current Freight Rate File :  File must contain the following columns:
			'Plant','Final Destination','Dest. Desc.','MODE','Direct Road Freight' 
		2) Destination Distance File : File must contain the following columns:
			'Direct Road Freight Rate','Description','Plant','Mode of Transport','Distance in KM'
		3) Percentage Increase/Decrease value obtained from Calculate Inc/Dec Rate

--> Afer Clicking on Submit button we get the result and we can download as well.
