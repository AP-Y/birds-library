from script import *; # Import all functions, variables, etc from script.py
import tkinter as tk; # Python GUI library
import tkinter.font;
from tkinter import ttk;
from PIL import ImageTk, Image;
from urllib.request import urlopen; # Python library for opening and reading content of URLs
from io import BytesIO;
import webbrowser; # Python library to use webbrowser
from autocompletion import AutocompleteCombobox; # File I found online that enables autocompletion for tkinter input widgets

# Since Python doesn't hoist functions, the order of functions as written is NOT the order they are executed in
# Basically, we make searchBy_Var (perform chooseSearchTerm()); make searchTerm_Var (perform checkFamily()); perform updateFamily() if needed; perform performSearch(); perform displayBird()

window = tk.Tk(); # Set up app window
window.title = 'Birds Library!';
window.geometry('600x600');
db_conn = connectDB();
style = ttk.Style();
style.theme_use('clam');
defaultFont = tk.font.nametofont('TkDefaultFont');
window.option_add('*Font', 'Times 12');

inputFrm = tk.Frame(); # Everyting user needs to input here
inputFrm.pack();

outputFrm = tk.Frame(); # Everyting program outputs here
outputFrm.pack();

def myRestart(): # Clear most of app
    inputFrmList = inputFrm.winfo_children();
    numInpWid = len(inputFrmList);
    if (numInpWid > 3): # Remove certain widgets from inputFrm
        inputFrmList[3].destroy();
        if (numInpWid > 4):
            inputFrmList[4].destroy();
    clearFrm(outputFrm);

restartBtn = tk.Button(master = inputFrm, text = 'Restart', font = 'Times 12 bold', command = myRestart);
restartBtn.pack(side = tk.TOP, padx = 3, pady = 3);

lifeList = []; # List of birdInfo user saves

def saveBird(birdInfo): # Append birdInfo to lifeList if bird not already saved
    if (birdInfo not in lifeList):
        lifeList.append(birdInfo);

def displayLifeList(): # Display all birds in lifeList
    clearFrm(outputFrm);
    for bird in lifeList:
        displayBird(bird);

lifeListBtn = tk.Button(master = inputFrm, text = 'Life List', font = 'Times 12 bold', command = displayLifeList);
lifeListBtn.pack(side = tk.TOP, padx = 3, pady = 3);

def clearFrm(frm): # Destory all widgets in frm; from https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
    for widget in frm.winfo_children():
        widget.destroy()

def makeComBox1(lblText, optList): # Create frame of lable and Combobox (fancy options menu with all values of optList as options); from https://www.geeksforgeeks.org/combobox-widget-in-tkinter-python/
    frm = tk.Frame(master = inputFrm);
    frm.pack();
    lbl = tk.Label(master = frm, text = lblText, font = 'Times 12 bold');
    lbl.pack();
    comBox = AutocompleteCombobox(frm)
    comBox.set_completion_list(optList)
    comBox.pack()
    comBox.focus_set()
    return comBox;
def makeComBox2(comBox, eventCommand): # Make it so comBox performs eventCommand when an option is selected
    comBox.bind('<<ComboboxSelected>>', eventCommand);

printNamesList = list((searchKeyDict['printName'] for searchKeyDict in list((searchKeyDict for searchKeyDict in searchKeysDict.values())))); # List printNames of all searchKeys

def chooseSearchTerm(event, searchBy):
    searchBy = searchKeysDict[list(searchKeysDict)[printNamesList.index(searchBy)]]; # Save user input as key of sub-dictionary in searchKeysDict that user wants to searchBy
    options = getOptions(searchBy['colName'], True, db_conn); # Select distinct values for user's searchBy
    searchTerm_Var = makeComBox1('What %s would you like to search for?' %(searchBy['printName']), options); # Ask user what searchTerm they want
    makeComBox2(searchTerm_Var, lambda event: checkFamily(event, searchBy, searchTerm_Var.get())); # When user select what searchTerm to use, check if they should also search by family

def checkFamily(event, searchBy, searchTerm):
    if (searchBy == searchKeysDict['order1']): # If user searched by order. . .
        options = getOptions(searchKeysDict['family']['colName'], ('UPPER(%s) = UPPER("%s")' %(searchKeysDict['order1']['colName'], searchTerm)), db_conn); # Select distinct families that match the user's given order
        if (len(options) > 1): # . . . and there are multiple families in that order
            familySearch_Var = makeComBox1(('What family in the %s order would you like to search in?' %(searchTerm)), options); # Ask user which family in that order they want to search in
            makeComBox2(familySearch_Var, lambda event: updateFamily(event, searchBy, searchTerm, familySearch_Var.get())); # When user select which family to search by, update searchTerm to match new family search
        else: # Else, go on to performSearch();
            performSearch(searchBy, searchTerm);
    else:
        performSearch(searchBy, searchTerm);

def updateFamily(event, searchBy, searchTerm, familySearch):
    searchBy = searchKeysDict['family'];
    searchTerm = familySearch;
    performSearch(searchBy, searchTerm);

def performSearch(searchBy, searchTerm):
    birdsList = sqlSearch('*', ('UPPER(%s) = UPPER("%s")' %(searchBy['colName'], searchTerm)), db_conn); # Select all values that match user's criteria
    clearFrm(outputFrm);
    for birdDict in birdsList: # Display all birds that match user's criteria
        displayBird(getBirdInfo(birdDict));

def displayBird(birdInfo):
    frm = tk.Frame(master = outputFrm, relief = 'ridge', borderwidth = 3); # Make frame for bird
    frm.pack(side = tk.LEFT, padx = 3, pady = 3);
    lbl = tk.Label(master = frm, text = '%s:\n%s' %(birdInfo['Common Name'], birdInfo['Scientific Name'])); # Make label with common and scientific name
    lbl.bind('<Button-1>', lambda event: webbrowser.open_new_tab(birdInfo['eBird Website'])); # Link eBird website to lbl
    lbl.pack(padx = 3, pady = 3);
    if (birdInfo['Image URL'] is not None): # If there is an image URL for bird
        page = urlopen(birdInfo['Image URL']); # Open the web picture and read it into a memory stream
        image = BytesIO(page.read()); # Convert to an image PIL can handle
        pilImg = Image.open(image); # Use PIL to open
        pilImg = pilImg.resize((150, 150)); # Resize the image
        tkImg = ImageTk.PhotoImage(pilImg); # Save as tk image
        imgLbl = tk.Label(master = frm, image = tkImg, width = 150, height = 150); # Put the image into an imgLbl
        imgLbl.image = tkImg;
        imgLbl.pack(padx = 3, pady = 3);
    saveBtn = tk.Button(master = frm, text = 'Save', command = lambda: saveBird(birdInfo)); # saveBtn to save this bird to lifeList
    saveBtn.pack(padx = 3, pady = 3);

searchBy_Var = makeComBox1('What would you like to search for birds by?', printNamesList); # Ask user what they want to searchBy
makeComBox2(searchBy_Var, lambda event: chooseSearchTerm(event, searchBy_Var.get())); # When user select what to searchBy, ask user what searchTerm

window.mainloop();
closeDB(db_conn);
