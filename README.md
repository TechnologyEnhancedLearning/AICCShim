# AICCShim
A shim, which allows SCORM courses to be accessed via AICC

To use this shim file it needs to be copied into the root folder of a SCORM course. The files of the SCORM course will need to have been stored in Azure file storage which is used by AICC Relay

Additionally the AICCShim.html file will need to be modified. The iframe src (towards the bottom of the file) will need to be set to the starting html page of the SCORM course. 
