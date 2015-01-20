# codeSample

This code snippet used for some json schema conversion. This conversion process can be initiated either as standalone
script or we can used it in a web application, here i am using it in both way's. The main input of this process is json
file that we want to convert into desired format.

Following is the description of each file.

1. routes.py
 - it contains all router of web application

2. models.py
 - it contains all models to store data into database.

2. json_packages_android_to_web.py
 - it is the main file that have code for json schema conversion. This can be also executed at standalone script.

3. handler.py
 -  it have the code for the case if we want to used the same conversion script in any web application. I am using the
 same script for schema conversion and after conversion of each record of input file i am saving the new schema into
 database.

The code contains only related methods. All library imports are removed for these files for readability purpose.