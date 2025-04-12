# Instructions

In order to run everything on Mac OS, type 'make run' in the command prompt, you will see the folders for the chunks generated as well as bob_received_file.txt with the data that bob received.

To clear everything for a rerun, type 'make clean' in the command prompt and all folders will be cleaned and processes will be terminated. Note that the terminals opened will not be closed - only terminated. PS: make clean does not delete the bob_received_file.txt once its generated however it will regenerate it everytime make run is called.

Please note : On a windows or Linux system, 'make all' will not work due to use of osascript for terminal automation, to run the project on windows or linux, refer to the makefile by typing 'make all' or 'make help'. Then do all the steps manually by opening new terminals and it should work as intended. 'make clean' can be used without issues on Windows and Linux too.

This Project for Computer Networks was developed by Aadil Chasmawala, Ashmit Mukherjee, Akshith Karthik and Lovnish Julka. The version on github is a cleaned version with 'make clean' command executed on it.
