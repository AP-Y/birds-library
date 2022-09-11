import pandas as pd;
import sqlite3; # Python package for SQL
import requests; # Python package for opening and reading content of URLs
from lxml import html; # Python package for scraping HTML

def printSpace():
    print('--------------------------------------------------');

def askYNQues(): # Print yes-no question and ask for user input; return True or False
    print('Please answer yes (Y) or no (N).');
    userInput = input();
    if (userInput.upper() in ('YES', 'Y')):
        return True;
    else:
        return False;

def printList(list): # Given parameter list, return string of list elements concatenated with punctuation
    string = '';
    for i in range(len(list)): # Loop through index i for length of list
        if (list[i] is None):
            continue;
        if (i == len(list) - 1):
            string += list[i];
        elif (i == len(list) - 2):
            string += list[i] + ', and ';
        else:
            string += list[i] + ', ';
    return string;

def askValidInput(checkValid): # Ask for user input until valid (check with checkValid(userInput) callback function parameter, which takes userInput and returns True if it is valid), then return valid input; from https://stackoverflow.com/questions/21943973/if-an-exception-is-raised-ask-again-for-input
    while True:
        userInput = input();
        if(checkValid(userInput)):
            return userInput;
        else:
            print('Your input was invalid. Please try again.');

def connectDB(): # Connect to birds.db SQL database (has 1 birds table) and return connection
    return sqlite3.connect('assets/birds.db');

def closeDB(db_conn): # Close the database at db_conn
    db_conn.close();

def sqlSearch(colName, whereStatement, db_conn): # Return list of dictionaries (of birds of colums) that match whereStatement
    return pd.read_sql('SELECT %s FROM birds WHERE %s ORDER BY %s' %(colName, whereStatement, (colName if (colName is not '*') else 'Primary_Com_Name')), db_conn).T.to_dict().values();

def getOptions(colName, whereStatement, db_conn): # Print user's options in colName given whereStatement and return list options
    options = pd.read_sql('SELECT DISTINCT %s FROM birds WHERE %s ORDER BY %s' %(colName, whereStatement, (colName if (colName is not '*') else 'Primary_Com_Name')), db_conn)[colName].values.tolist();
    options = [option for option in options if option is not None]; # Remove None values from options
    return options;

def getBirdInfo(birdDict): # From birdDict and eBird website, get information about bird and put into birdInfo dictionary
    birdInfo = {
        'Species Code': birdDict['Species_Code'],
        'Common Name':birdDict['Primary_Com_Name'],
        'Scientific Name': birdDict['Sci_Name'],
        'Domain': 'Eukarya',
        'Kingdom': 'Animalia',
        'Phylum': 'Chordata',
        'Class': 'Aves',
        'Order': birdDict['Order1'],
        'Family': birdDict['Family'],
        'Genus': birdDict['Sci_Name'].split(" ", 1)[0], # Split the scientific name to get genus (first part) and species (second part)
        'Species': birdDict['Sci_Name'].split(" ", 1)[1].capitalize(),
        'eBird Website': 'https://ebird.org/species/%s' %(birdDict['Species_Code']), # Link to website about that bird
        'Birds of the World Website': 'https://birdsoftheworld.org/bow/species/%s' %(birdDict['Report_As'] if birdDict['Report_As'] else birdDict['Species_Code']), # Birds of the World does not work with some of the more specific Species_Code, so use Report_As
        'Description': None,
        'Image URL': None
    }
    page = requests.get(birdInfo['eBird Website']); # Open eBird website for that bird
    tree = html.fromstring(page.content); # Read the HTML
    try: # Attempt the following code
        description = str(tree.xpath('normalize-space(/html/head/meta[@name="description"]/@content)')); # Get description of that bird from HTML <meta name="description"> element
        if (description and not(description.startswith('Learn about '))): # If there truely is a description, print it
            birdInfo['Description'] = description;
    except: # If there are any errors, don't execute it (just pass)
        pass;
    try:
        imageURL = tree.xpath('//img[1]')[0].attrib['src']; # Get src for first image of that bird in HTML
        if (imageURL):
            birdInfo['Image URL'] = imageURL + '.png';
    except:
        pass;
    return birdInfo;

def displayBirdTerminal(birdInfo): # Display birdInfo properties using print-statements
    printSpace();
    for key, value in birdInfo.items():
        if (value is not None):
            print('%s: %s' %(key, value));
    printSpace();

searchKeysDict = { # This dictionary of dictionaries links each search key's printable form, column name, and index (for ease of typing)
    'comName': {
        'printName': 'common name',
        'colName': 'Primary_Com_Name',
        'ind': 0
    },
    'sciName': {
        'printName': 'scientific name',
        'colName': 'Sci_Name',
        'ind': 1
    },
    'order1': {
        'printName': 'order',
        'colName': 'Order1',
        'ind': 2
    },
    'family': {
        'printName': 'family',
        'colName': 'Family',
        'ind': 3
    }
}

lifeList = []; # List of Species_Codes of birds user saved

def runTerminal():
    printSpace();
    print('Welcome to Birds Library!');
    print('Would you like to search for birds by %s (%s), %s (%s), %s (%s), or %s (%s)?' %(searchKeysDict['comName']['printName'], searchKeysDict['comName']['ind'], searchKeysDict['sciName']['printName'], searchKeysDict['sciName']['ind'], searchKeysDict['order1']['printName'], searchKeysDict['order1']['ind'], searchKeysDict['family']['printName'], searchKeysDict['family']['ind'])); # %s act as string placeholders, which hold printName and ind for each searchKey
    searchKeyList = list(searchKeysDict);
    searchBy = searchKeysDict[searchKeyList[int(askValidInput(lambda userInput: True if (int(userInput) in range(len(searchKeyList))) else False))]]; # Save user input as key of sub-dictionary in searchKeysDict that user wants to searchBy

    printSpace();
    print('What %s would you like to search for?' %(searchBy['printName']));
    options = getOptions(searchBy['colName'], True, db_conn); # Select distinct values for user's searchBy
    print('The options include %s.' %(printList(options)));
    searchTerm = askValidInput(lambda userInput: True if userInput.upper() in (option.upper() for option in options) else False); # Save user input as string of term to search

    if (searchBy == searchKeysDict['order1']): # If user searched by order. . .
        options = getOptions(searchKeysDict['family']['colName'], ('UPPER(%s) = UPPER("%s")' %(searchKeysDict['order1']['colName'], searchTerm)), db_conn); # Select distinct families that match the user's given order
        if (len(options) > 1): # . . . and there are multiple families in that order
            printSpace();
            print('Since you searched by %s, would you also like to search by %s?' %(searchKeysDict['order1']['printName'], searchKeysDict['family']['printName'])); # Ask if they also want to search by family
            familySearchBool = askYNQues();
            if (familySearchBool): # If user decieded to search by family, update searchBy and searchTerm
                print('The options include %s.' %(printList(options)));
                searchTerm = askValidInput(lambda userInput: True if userInput.upper() in (option.upper() for option in options) else False); # Save user input as string of term to search
                searchBy = searchKeysDict['family'];

    birdsList = sqlSearch('*', ('UPPER(%s) = UPPER("%s")' %(searchBy['colName'], searchTerm)), db_conn); # Select all values that match user's criteria
    speciesCodes = [d['Species_Code'] for d in birdsList if 'Species_Code' in d]; # List of speciesCodes that match user's criteria; From https://stackoverflow.com/questions/7271482/getting-a-list-of-values-from-a-list-of-dicts

    for birdDict in birdsList: # Display all birds that match user's criteria
        displayBirdTerminal(getBirdInfo(birdDict));

    while True: # Allow user to save as many birds as they want
        printSpace();
        print('Would you like to save a bird?');
        saveBirdBool = askYNQues();
        if (saveBirdBool): # If user decieded to save a bird, append bird's Species_Code to lifeList
            print('Please input the bird\'s species code.');
            saveCode = askValidInput(lambda userInput : True if userInput.upper() in (speciesCode.upper() for speciesCode in speciesCodes) else False); # Save user input as string of Species_Code of bird to save
            birdName = list(sqlSearch('Primary_Com_Name', ('UPPER(Species_Code) = UPPER("%s")' %(saveCode)), db_conn))[0]['Primary_Com_Name'];
            if (saveCode not in lifeList): # If that saveCode has not already been saved in lifeLife, append it to lifeList
                lifeList.append(saveCode);
                print('You have successfully saved the %s to your life list.' %(birdName));
            else:
                print('You have already saved the %s to your life list.' %(birdName));
        else:
            break;

    printSpace();
    print('Would you like to see your saved birds?');
    seeSavedBirdsBool = askYNQues();
    if (seeSavedBirdsBool): # If user wants to seeSavedBirds, display saved birds
            for bird in lifeList: # For each bird in lifeList, get birdDict and display that bird
                birdDict = list(sqlSearch('*', ('UPPER(Species_Code) = UPPER("%s")' %(bird)), db_conn))[0];
                displayBirdTerminal(getBirdInfo(birdDict));

# db_conn = connectDB();
# runTerminal();
# closeDB(db_conn);
