import argparse
import json
import sys

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-u', action='store', dest='user',
                    help='The user you are searching for')
parser.add_argument('-k', action='store', dest='keywords',
                    help='The tags to search for')
parser.add_argument('-x', action='store_true', dest='apply_tag',
                    help='Apply tag to user')
args = parser.parse_args()

# Load JSON files
with open('windowsinfo.json') as json_file:
    data = json.load(json_file)

with open('credentials.json') as cred_file:
    cred_data = json.load(cred_file)

# Search for user
if args.user:
    for user in data:
        if user.get('type') == 'User' and user.get('name', '').find(args.user) != -1:
            print(user)


if args.keywords:
    # Search for tags
    for cred in cred_data:
        if cred.get('tag', '').find(args.keywords) != -1:
            print('Keyword found in tag', cred['tag'])
            # Get user associated with tag
            for tags in data:
                if cred.get('tags') == 'User' and cred.get('tag', '').find(cred['tag']) != -1:
                    print(tags)
                    # Check if -x flag has been set
                    if args.apply_tag:
                        # Create new authlinks.json file
                        with open('authlinks.json', 'a+') as authlinks_file:
                            # Load existing authlinks file data
                            try:
                                auth_data = json.load(authlinks_file)
                            except:
                                auth_data = []

                            # Create new object for user/tag
                            new_auth_data = {
                                'user': user,
                                'tags': cred['tag']
                            }

                            # Append new object to existing authlinks file data
                            auth_data.append(new_auth_data)

                            # Write object to file
                            json.dump(auth_data, authlinks_file)

else:
    # List all tags
    for cred in cred_data:
        print('Tag:', cred['tag'])