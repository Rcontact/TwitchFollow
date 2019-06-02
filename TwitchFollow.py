import requests
import json
import sys
from demjson import decode

# OWNER: RB

#USING NEW TWITCH API ##NOT API V5 https://dev.twitch.tv/docs/api/reference/#get-users-follows

url = "https://api.twitch.tv/helix/users/follows"  # Collecting user follower information using NEW Twitch API
print(url)

json_after = "" ## Pagination Value, left blank for initilisation
json_name = input("Please Enter Username: ") ## Isn't case sensitive. Is the username of the user required for analysis
json_tf = "to_id" ## can be changed to "from_id" to collect the people the user followers.

#------------To find Name of the id being scraped----------------
#------------ GET called made using POSTMAN----------------------

urls = "https://api.twitch.tv/helix/users" # Collecting user information using NEW Twitch API
querystrings = {"login":json_name}
headerss = {
    'Authorization': "", ############ Unique to developer scraping code
    'cache-control': "no-cache",
    'Postman-Token': ""    ######## Token Made up when Making Postman Call 
    }

#-------------Below is used to display in terminal output---------- 
responses = requests.request("GET", urls, headers=headerss, params=querystrings)
json_datas = responses.json() #Output to Twitch Unique API, similar to Json, uses ' instead of "
json_id = json_datas['data'][0]['id'] 
json_btype = json_datas['data'][0]['broadcaster_type']
json_views = json_datas['data'][0]['view_count']


#-------------To Find who Follows this id------------------------
#------------ GET called made using POSTMAN----------------------
querystring = {json_tf:json_id,"after":json_after}    
headers = {
    'Authorization': "", ########## Unique to developer scraping code
    'Cache-Control': "no-cache",
    'Postman-Token': "" Token Made up when Making Postman Call 
    }

response = requests.request("GET", url, headers=headers, params=querystring)

# 
# Similar to before, output is not in proper json form, however can be manipulated similarly
# 

json_data = response.json()
json_total = json_data['total'] #returns value from total packet from get call


#------------First loop value to find all id's that follow the id of interest
print('ID\'s that follow ' + str(json_name)) 


#-----Input must not be in quotations, or not abide by file naming rules.
filename = input("Please Enter New Filename: Name_DD_MM_YYYY.json ")

#--- Creates new file if it doesnt exist with input name ----
file = open(filename,"w")



#------------ Twitch API only allows for 20 values per page request------------
#------------ At Time of development, API Defaults allow for 20, however maximum limit is 100.
counter = 0

# Provides number of iterations based on number of followers user has, divided by page size based on
# Floor Division. eg 0 < 1600 + 19 // 20 == 0 < 80
# This allows for the application run once more for the values less than 20.
while counter < ((json_total + 20 - 1) // 20):  
    # Will return in with the json packet data inside the 'total' packet. Hence, the packet needs to separated.
    formatted_follow = json_data['data'][:20] # First 20 values in packet before pagination.
    python_dict = json.dumps(formatted_follow) #Converts the information into a string converts the '' into ""


  #  print(python_dict) 
  # # **uncomment to see output in terminal**
    
    file.write(str(python_dict)) #Write to file the string
    json_after = "" + str(json_data['pagination']['cursor']) # Give json_after the cursor value to then be re-input into the call 

    #---REPEATED FROM INITIATION VALUES---------
    querystring = {json_tf:json_id,"after":json_after} 
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = response.json()
    json_total = json_data['total']
    counter += 1 ##increment counter




# --- Outputs User Information for reader in Terminal: follower count, user ID, Name, account type, View count
print()
print('Follow total: ' + str(json_total))
print('User ID: ' + str(json_id))
print('User Name: ' + json_name)
print('Broadcaster Type: ' + str(json_btype))
print('View Count: ' + str(json_views))

file.close()



#---- File Cleaner found on stacked overflow----
# Used to tackle nature of data packet with leading '[' and tailing ']'.
# allowing  user to easily replace with ',' meaning that all values can be exported on one json file.
# NOTE # At time of development, this error was not possible at run time, due to packet not being recognised as a string
# ---- # Was unable to write to file with correction as payload would output with [*all user data*] and ',' would need to be
# ---- # put in between ']['
# Hence, Two files are made, naturally original file should be removed to limit space used by program.

infile = filename
outfile = "cleaned_"+filename

delete_list = ['][']
fin = open(infile)
fout = open(outfile, "w+")
for line in fin:
    for word in delete_list:
        line = line.replace(word, ',')
    fout.write(line)
fin.close()
fout.close()
