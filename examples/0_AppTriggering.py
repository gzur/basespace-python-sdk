import sys
sys.path.append('/home/mkallberg/workspace/basespace-python-sdk/src/')
from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
import helper
import webbrowser
import time

"""
This script demonstrates how to retrieve the AppSession object produced 
when a user initiates an app. Further it's demonstrated how to automatically
generate the scope strings to request access to the data object (a project or a sample)
that the app was triggered to analyze. 

NOTE: You will need to fill client values for your app below
"""

# initialize an authentication object using the key and secret from your app

# FILL IN WITH YOUR APP VALUES HERE!
client_key                 = ""
client_secret              = ""
AppSessionId               = ""

# test if client variables have been set
helper.checkClientVars({'client_key':client_key,'client_secret':client_secret,'AppSessionId':AppSessionId}) 

BaseSpaceUrl               = 'https://api.cloud-endor.illumina.com/'
version                    = 'v1pre3/'

# First we will initialize a BaseSpace API object using our app information and the appSessionId
BSapi = BaseSpaceAPI(client_key, client_secret, BaseSpaceUrl, version, AppSessionId)

# Using the basespaceApi we can request the appSession object corresponding to the AppSession id supplied
myAppSession = BSapi.getAppSession()
print myAppSession

# An app session contains a referal to one or more appLaunchObjects which reference the data module
# the user launched the app on. This can be a list of projects, samples, or a mixture of objects  
print "\nType of data the app was triggered on can be seen in 'references'"
print myAppSession.References

# We can also get a handle to the user who started the AppSession
print "\nWe can get a handle for the user who triggered the app\n" + str(myAppSession.UserCreatedBy)

# Let's have a closer look at the appSessionLaunchObject
myReference =  myAppSession.References[0]
print "\nWe can get out information such as the href to the launch object:"
print myReference.HrefContent
print "\nand the specific type of that object:"
print myReference.Type


# Now we will want to ask for more permission for the specific reference object
print "\nWe can get out the specific project objects by using 'content':" 
myReference =  myReference.Content
print myReference
print "\nThe scope string for requesting write access to the reference object is:"
print myReference.getAccessStr(scope='write')

# We can easily request write access to the reference object so our App can start contributing analysis
# by default we ask for write permission to and authentication for a devise
accessMap = BSapi.getAccess(myReference)
print "\nWe get the following access map"
print accessMap

## PAUSE HERE
# Have the user visit the verification uri to grant us access
print "\nPlease visit the uri within 15 seconds and grant access"
print accessMap['verification_with_code_uri']
webbrowser.open_new(accessMap['verification_with_code_uri'])
time.sleep(15)
## PAUSE HERE

# Once the user has granted us access to objects we requested we can
# get the basespace access token and start browsing simply by calling updatePriviliges
# on the baseSpaceApi instance    
code = accessMap['device_code']
BSapi.updatePrivileges(code)
print "\nThe BaseSpaceAPI instance was update with write privileges"

# for more details on access-requests and authentication and an exmaple of the web-based case see example 1_Authentication.py 

