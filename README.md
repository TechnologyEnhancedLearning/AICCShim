# AICCShim
A shim, which allows SCORM courses to be accessed via AICC

To use this shim file it needs to be copied into the root folder of a SCORM course. The files of the SCORM course will need to have been stored in Azure file storage which is used by AICC Relay

Additionally the AICCShim.html file will need to be modified. The iframe src (towards the bottom of the file) will need to be set to the starting html page of the SCORM course. 

## Setup utilities
Two python utility scripts have been included in this repo. prepare_shim.py should be run in the root folder of a SCORM package. The AICCShim.html file must have already been copied into this folder. Running this utility 'python prepare_shim.py' will find the start point in the SCORM imsmanifest.xml file and insert the start point into the AICCShim.html file

The second utility prepare_all_shims.py is designed to batch process all existing SCORM courses, which are held in folders under the current folder. The AICCShim.html file will need to be present in the current folder. Running this utiity 'python prepare_all_shims.py' will copy AICCShim.html into each subfolder which is a valid SCORM resource and will update the AICCShim.html with the start point extracted from th imsmanifest.xml file. As SCORM course data is usually held in an Azure file share, this file share should be mounted on a dev machine as a drive (Z:), so that the python code can be run on the dev machine.

## Setup in Moodle
To use the shim to access a SCORM course via AICC in Moodle, do the following:
1. Add a new SCORM package activity to an existing course (create the course if one does not yet exist).
2. The Package Type needs to be External AICC URL.
3. The URL needs to point to the appropriate AICC relay for the environment that you are using. For example, a relay has been set up for the proof of concept at https://contentpocwindows.azurewebsites.net . The next part of the URL should be AICC/InitialiseRelay?CONTENT_URL= this should then be followed by the path to the content. For example /lhcontent/adapt-without-aicc/AICCShim.html . 
4. Other settings should be set up as required.