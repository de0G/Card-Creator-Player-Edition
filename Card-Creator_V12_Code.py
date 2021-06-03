import tkinter as tk
from tkinter import font
from tkinter.messagebox import showerror, askquestion, showinfo
import tkinter.scrolledtext as st
import os
from cryptography.fernet import Fernet
from datetime import datetime

def ChooseColour():
    global decider
    global cardColours
    global colour
    colour = cardColours[decider % 2]
    decider += 1
    SetColour(colour)

def SeeCards(normalFont, inputFont):
    try:
        name = nameEntry.get().strip()

        if name == "":
            showerror("ERROR: Can't get Cards", "You must enter the name of the deck that you want to view")
        else:
            try:
                file = f"{name}.txt"
                path = os.path.join(deckDirectory, file)

                decrypt(path)
                
                deck = open(path, "r")
                cards = []
                blackCards = []
                whiteCards = []

                for card in deck:
                    cards.append(card.strip())
                    if "_" in card:
                        blackCards.append(card.strip())
                    else:
                        whiteCards.append(card.strip())

                deck.close()
                
                whiteNum = len(whiteCards)
                blackNum = len(blackCards)
                
                cardWindow = tk.Toplevel()
                cardWindow.iconbitmap(os.path.join(dataDirectory, "logo.ico"))
                cardWindow.title(f"Deck: {name.title()}")

                cardCanvas = tk.Canvas(cardWindow, height=480, width=600) #previous height = 350
                cardCanvas.pack()

                cardTitle = tk.Label(cardWindow, text = f"Cards for the '{name}' deck", font = ("Trebuchet MS", 23))
                cardTitle.place(anchor = "n", relx = 0.5, rely = 0.02, relheight = 0.10, relwidth = 1)

                whiteLabel = tk.Label(cardWindow, text = f"White Cards: {whiteNum}", font = normalFont)
                whiteLabel.place(anchor = "nw", relx = 0.03, rely = 0.12, relheight = 0.1, relwidth = 0.3)

                blackLabel = tk.Label(cardWindow, text = f"Black Cards: {blackNum}", font = normalFont)
                blackLabel.place(anchor = "nw", relx = 0.52, rely = 0.12, relheight = 0.1, relwidth = 0.3)

                whiteTextbox = st.ScrolledText(cardWindow, font = inputFont)
                whiteTextbox.place(anchor = "nw", relx = 0.03, rely = 0.21, relheight = 0.5, relwidth = 0.46)

                blackTextbox = st.ScrolledText(cardWindow, bg = "black", fg = "white", font = inputFont)
                blackTextbox.place(anchor = "nw", relx = 0.52, rely = 0.21, relheight = 0.5, relwidth = 0.46)

                whiteText = ""
                blackText = ""

                counter = 1
                
                for card in whiteCards:
                    whiteText += f"{str(counter)}. {card}\n\n"
                    counter += 1

                counter = 1
                
                for card in blackCards:
                    blackText += f"{str(counter)}. {card}\n\n"
                    counter += 1

                if len(whiteCards) > len(blackCards):
                    maximum = len(whiteCards)
                else:
                    maximum = len(blackCards)

                whiteTextbox.insert(tk.INSERT, whiteText)
                blackTextbox.insert(tk.INSERT, blackText)
                
                whiteTextbox.configure(state = "disabled")
                blackTextbox.configure(state = "disabled")

                removeLabel = tk.Label(cardWindow, text = "Remove Card", font = ("Trebuchet MS", 18))
                removeLabel.place(anchor = "n", relx = 0.5, rely = 0.72, relheight = 0.09, relwidth = 1)

                cardRemovalColour = tk.StringVar()
                cardRemovalColour.set("white")

                whiteRemove = tk.Radiobutton(cardWindow, text = "Remove a White Card", variable = cardRemovalColour, value = "white", font = inputFont)
                whiteRemove.place(anchor = "nw", relx = 0.03, rely = 0.78, relheight = 0.1, relwidth = 0.3)

                blackRemove = tk.Radiobutton(cardWindow, text = "Remove a Black Card", variable = cardRemovalColour, value = "black", font = inputFont)
                blackRemove.place(anchor = "nw", relx = 0.025, rely = 0.86, relheight = 0.1, relwidth = 0.3)

                indexLabel = tk.Label(cardWindow, text = "Select Card Index:", font = ("Calibri", 15))
                indexLabel.place(anchor = "nw", relx = 0.33, rely = 0.81, relheight = 0.06, relwidth = 0.3)

                indexBox = tk.Spinbox(cardWindow, from_ = 1, to = maximum, font = inputFont)
                indexBox.place(anchor = "n", relx = 0.5, rely = 0.87, relheight = 0.07, relwidth = 0.3)

                removeButton = tk.Button(cardWindow, text = "Remove\nCard", font = buttonFont, command=lambda:RemoveCard(whiteCards, blackCards, indexBox, path, cardRemovalColour, normalFont, inputFont, maximum, cardWindow))
                removeButton.place(relx = 0.69, rely = 0.81, relheight = 0.14, relwidth = 0.27, anchor = "nw")

                CacheSave(name)
                encrypt(path)

                cardWindow.mainloop()
            except Exception as errorMessage:
                log(f"ERROR: {errorMessage}")
                showerror("ERROR: Can't get Cards", f"The deck '{name}' does not exist")
    except Exception as errorMessage:
        log(f"CRITICAL ERROR: {errorMessage}")

def SetColour(cardColour):
    if cardColour == "white":
        bg = "white"
        fg = "black"
    else:
        bg = "black"
        fg = "white"

    nameEntry['bg'] = bg
    nameEntry['fg'] = fg

    cardTextbox['bg'] = bg
    cardTextbox['fg'] = fg

    cardLabel['text'] = f"Card ({cardColour.title()}):"

def CheckInput():
    try:
        name = nameEntry.get().strip()
        card = cardTextbox.get("1.0","end-1c")

        illegal = ["(", ")", "[", "]", ":", " ", "{", "}", "\\", "/", "."]

        valid = True

        for criminal in illegal:
            if criminal in name:
                valid = False

        underscore = False
        nonUnderscore = False

        if "_" in card:
            underscore = True

        splitCards = card.split("\n")

        for split in splitCards:
            if ("_" not in split.strip()) and (split.strip() != ""):
                nonUnderscore = True
        
        if name == "":
            showerror("ERROR: Can't Add Card","You must enter your DECK NAME")
        elif card.strip() == "":
            showerror("ERROR: Can't Add Card","You must enter your CARD")
        elif not valid:
            showerror("ERROR: Can't Add Card","Deck name has an illegal character (e.g. spaces, colons, slashes, etc.)\n\nTry replacing spaces with underscores")
        elif underscore and colour == "white":
            showerror("ERROR: Can't Add Card","White Cards cannot have an underscore")
        elif nonUnderscore and colour == "black":
            showerror("ERROR: Can't Add Card","All Black Cards must have at least one underscore to represent the responses to the card")
        else:
            try:
                continu = "yes"
                file = f"{name}.txt"
                path = os.path.join(deckDirectory, file)
                deck = open(path, "r")
                newDeck = False
            except Exception as errorMessage:
                log(f"ERROR: {errorMessage}")
                continu = askquestion("Deck does not exist", f"The deck '{name}' does not exist, do you want to create a new one?")
                newDeck = True
            if continu == "yes":
                deck = open(path, "a+")

                if "manual-encrypt" in card:
                    encrypt(path)
                    log(f"DECK '{name}' MANUALLY ENCRYPTED")
                    showinfo("Manual Encryption Successful", f"The deck '{name}' was successfully manually encrypted!")
                    cardTextbox.delete("1.0", "end")
                elif "manual-decrypt" in card:
                    decrypt(path)
                    log(f"DECK '{name}' MANUALLY DECRYPTED")
                    showinfo("Manual Decryption Successful", f"The deck '{name}' was successfully manually decrypted!")
                    cardTextbox.delete("1.0", "end")
                else:
                    if not newDeck:
                        decrypt(path)
                    else:
                        log(f"NEW DECK '{name}' CREATED")
                    
                    for separated in splitCards:
                        if separated.strip() != "":
                            deck.write(SuperfluousRemover(separated.lower()) + "\n")
                            log(f"ADDED {colour.upper()} CARD '{separated.lower()}' TO DECK '{name}'")
                            
                    deck.close()
                    cardTextbox.delete("1.0", "end")

                    CacheSave(name)
                    encrypt(path)
    except Exception as errorMessage:
        log(f"CRITICAL ERROR: {errorMessage}")

def CacheSave(filename):
    path = os.path.join(dataDirectory, "cache.txt")
    cache = open(path, "w")
    cache.write(filename)
    cache.close()

def GetCache():
    path = os.path.join(dataDirectory, "cache.txt")
    cache = open(path, "r")
    lastFile = cache.read()
    
    return lastFile

def encrypt(file):
    keyFile = open(os.path.join(dataDirectory, "key.key"), "rb")
    key = keyFile.read()
    key = key[:-1]
    keyFile.close()

    with open(file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(file, 'wb') as f:
        f.write(encrypted)

    log(f"'{file}' AUTOMATICALLY ENCRYPTED")

def decrypt(file):
    keyFile = open(os.path.join(dataDirectory, "key.key"), "rb")
    key = keyFile.read()
    key = key[:-1]
    keyFile.close()
    
    f = open(file, 'rb')
    data = f.read()
    f.close()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    f = open(file, 'wb')
    f.write(decrypted)
    f.close()

    log(f"'{file}' AUTOMATICALLY DECRYPTED")

def log(message):
    logFile = open(os.path.join(dataDirectory, "log.txt"), "a+")
    logTime = datetime.now().strftime("[%d/%m/%y %H:%M:%S]")
    logFile.write(f"{logTime} {message}\n")
    logFile.close()

def SuperfluousRemover(card):
    cull = False
    new = ""
    
    for letter in card:
        if cull:
            if letter == "_":
                addition = ""
            else:
                addition = letter
                cull = False
        else:
            addition = letter
            
            if letter == "_":
                cull = True
                
        new += addition

    return new

def RemoveCard(whiteCards, blackCards, indexBox, path, cardRemovalColour, normalFont, inputFont, maximum, cardWindow):
    removeColour = cardRemovalColour.get()

    if maximum > 1:
        index = int(indexBox.get()) - 1
    else:
        index = 0
    
    try:
        tempWhite = whiteCards.copy()
        tempBlack = blackCards.copy()
        
        if removeColour == "white":
            remove = whiteCards[index]
            tempWhite.pop(index)
        else:
            remove = blackCards[index]
            tempBlack.pop(index)

        certain = askquestion("Are you Sure?", f"Are you sure that you want to remove the {removeColour.upper()} card:\n\n'{remove}'\n\nfrom the deck?")
        
        if certain == "yes":
            counter = 0

            deck = open(path, "w")
            
            for card in tempWhite:
                counter += 1
                deck.write(card + "\n")

            for card in tempBlack:
                counter += 1
                deck.write(card + "\n")

            deck.close()
            
            if counter == 0:
                os.remove(path)
                showinfo("Entire Deck Successfully Removed", f"The entire deck has been deleted as it now contains no cards")
                cardWindow.destroy()
            else:
                encrypt(path)
                showinfo("Card Successfully Removed", f"The card '{remove}' has been successfully removed")
                cardWindow.destroy()
                SeeCards(normalFont, inputFont)
    except:
        showerror("ERROR: Can't Remove Card", f"There is no {removeColour.title()} Card at index {index}")
        
try:
    version = "1.3"
    dataDirectory = f"{os.getcwd()}\\program_files"
    deckDirectory = f"{os.getcwd()}\\Decks"

    root = tk.Tk()
    root.title(f"deOG's Card-Creator {version}")
    root.iconbitmap(os.path.join(dataDirectory, "logo.ico"))

    cardColours = ["white","black"]
    decider = 0

    backgroundColour = "black"
    textColour = "white"

    w_height = 450
    w_width = 550

    normalFont = ("Calibri", 20)
    inputFont = ("Calibri", 13)
    buttonFont = ("Calibri", 15)

    canvas = tk.Canvas(root, height=w_height, width=w_width)
    canvas.pack()

    versionLabel = tk.Label(root, text = "[Player Edition]", font = ("Trebuchet MS", 13))
    versionLabel.place(anchor = "n", relx = 0.57, rely = 0.17, relheight = 0.05, relwidth = 0.6)

    titleLabel = tk.Label(root, text = "The Card-Creator", font = ("Trebuchet MS", 30))
    titleLabel.place(anchor = "n", relx = 0.57, rely = 0.06, relheight = 0.1, relwidth = 0.6)

    humanityLogo = tk.PhotoImage(file = os.path.join(dataDirectory, "humanityLogo.png")).subsample(3,3)
    humanityLabel = tk.Label(root, image = humanityLogo)
    humanityLabel.place(anchor = "n", relx = 0.2, rely = 0.03, relheight = 0.2, relwidth = 0.15)

    nameLabel = tk.Label(root, text = "Deck Name:", font = normalFont)
    nameLabel.place(anchor = "nw", relx = 0.03, rely = 0.24, relheight = 0.1, relwidth = 0.25)

    nameEntry = tk.Entry(root, bg = backgroundColour, fg = textColour, font = inputFont, cursor = "xterm")
    nameEntry.place(relx = 0.03, rely = 0.34, relwidth = 0.7, relheight = 0.1, anchor = "nw")

    nameEntry.insert(0, GetCache())

    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html - Shows all mouse cursor options with images

    cardLabel = tk.Label(root, text = "Card (Black):", font = normalFont)
    cardLabel.place(anchor = "nw", relx = 0.02, rely = 0.47, relheight = 0.06, relwidth = 0.3)

    cardTextbox = tk.Text(root, bg = backgroundColour, fg = textColour, font = inputFont)
    cardTextbox.place(relx = 0.03, rely = 0.56, relwidth = 0.7, relheight = 0.36, anchor = "nw")

    currentButton = tk.Button(root, text = "Add\nCard(s)", font = buttonFont, command=lambda:CheckInput())
    currentButton.place(relx = 0.86, rely = 0.30, relheight = 0.18, relwidth = 0.2, anchor = "n")

    colourButton = tk.Button(root, text = "Change\nCard\nColour", font = buttonFont, command=lambda:ChooseColour())
    colourButton.place(relx = 0.86, rely = 0.52, relheight = 0.18, relwidth = 0.2, anchor = "n")

    saveButton = tk.Button(root, text = "See\nDeck", font = buttonFont, command=lambda:SeeCards(normalFont, inputFont))
    saveButton.place(relx = 0.86, rely = 0.74, relheight = 0.18, relwidth = 0.2, anchor = "n")

    versionLabel = tk.Label(root, text = f"Version: {version}", font = ("Calibri", 15))
    versionLabel.place(anchor = "nw", relx = 0.01, rely = 0.93, relheight = 0.06, relwidth = 0.23)

    ChooseColour()

    root.mainloop()
except Exception as errorMessage:
    log(f"CRITICAL ERROR: {errorMessage}")
