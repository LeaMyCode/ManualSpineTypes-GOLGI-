close("*");

//Open folders (first for the images you want to analyse, second to save the treshold images and the excel files with the results; Important: first select the spine width, then the spine length and afterwards the length of the dendrit) 
dir1 = getDirectory("Choose Source Directory ");
dir2 = getDirectory("Chooose Destination Directory ");
list = getFileList(dir1);
//setBatchMode(true);
//Choosing the image which should be opened first (DAPI)
for (i=0; i<list.length; i++) {
	showProgress(i+1, list.length);
	if(list[i].matches('.*.czi')|| list[i].matches('.*.tif')|| list[i].matches('.*.oif')) {
	picture = list[i];
	open(dir1 + picture);
	
	title_definite = getTitle();
//Information for the user
		setTool("polyline");
		waitForUser("First select the width of a spine, then its length and add to the ROI manager. Lastly, select the dendrit length and add to the ROI manager.");
//Set Measurments
		run("Set Measurements...", "area mean min redirect=None decimal=3");
//Measure length of all spine data
		n = roiManager('count');
		for (j = 0; j < n; j++) {
    		roiManager('select', j);
    		run("Measure");
		}	
//Save all ROIS
		roiManager('select', "*");
		roiManager("Save", dir2 + title_definite + ".zip");
//Closes all ROIs
    	selectWindow("ROI Manager");
    	close();
//Transfer of the measurments into a excel file and save
		selectWindow("Results");
		saveAs("Results", dir2 + title_definite + ".csv");
//Close and or reset everything for the next image
		roiManager("reset");
		close("*");
		if (isOpen("Results")) {
		         selectWindow("Results");
		         run("Close");}
		if (isOpen("Log")) {
		         selectWindow("Log");
		         run("Close");
		}	
		if (isOpen("RoiManager")) {
		         selectWindow("RoiManager");
		         run("Close");
		}		
		
	}
}
waitForUser("Your analysis in Fiji is finished.");



