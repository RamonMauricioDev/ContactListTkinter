import tkinter as tk
from tkinter import messagebox
import json
import os
from PIL import Image, ImageTk

class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

class ContactList:
    def __init__(self, root):
        #Main properties
        self.root = root
        self.root.title("Contact List")
        self.root.geometry("448x448")
        self.root.minsize(448, 448)
        self.root.maxsize(448, 448)
        self.contactList = []

        self.render_top_frame()
        self.render_contact_frame()

    #Will add a new single contact in the contactList
    def add_new_contact(self, name, phone):
        if name and phone:
            try:
                phone = int(phone)
                contact = Contact(name, phone)
                self.contactList.append(contact)
                self.save_contact()
                self.createContactWindow.destroy()
            except ValueError:
                messagebox.showwarning("Something went wrong", "The phone entry only allows numbers!")
        else:
            messagebox.showwarning("Something went wrong", "Fill all entries!")

    #Save a json file with all contacts in contactList
    def save_contact(self):
        self.contactListFrame.destroy()

        with open("contacts.json", "w") as f:
            json.dump([contact.__dict__ for contact in self.contactList], f)

        self.render_contact_frame()

    def create_contact_window(self):
        if len(self.contactList) >= 6:
            messagebox.showwarning("Full list", "The maximum contact it's 6!")
            return None
        
        self.createContactWindow = tk.Toplevel()
        self.createContactWindow.geometry("260x120")
        self.createContactWindow.title("Create Contact")
        self.createContactWindow.columnconfigure((0, 1), weight=1)
        self.createContactWindow.rowconfigure((0, 1, 2), weight=1)

        tk.Label(self.createContactWindow, text="Name: ", font="Arial 14").grid(column=0, row=0)
        tk.Label(self.createContactWindow, text="Phone: ", font="Arial 14").grid(column=0, row=1)
        name = tk.Entry(self.createContactWindow)
        name.grid(column=1, row=0)
        phone = tk.Entry(self.createContactWindow)
        phone.grid(column=1, row=1)

        tk.Button(self.createContactWindow, text="Create Contact", command= lambda: self.add_new_contact(name.get(), phone.get())).grid(column=1, row=2, sticky="nswe", padx=5, pady=5)

    #It will render the contact frame
    def render_contact_frame(self):
        #Contact List Frame
        self.contactListFrame = tk.Frame(root)
        self.contactListFrame.columnconfigure((0), weight=0)
        self.contactListFrame.columnconfigure((1), weight=1)
        self.contactListFrame.rowconfigure((0, 1, 2, 3, 4, 5), weight=0)

        #Add Button
        self.pillow_image = Image.open('plus.png')
        self.pillow_image = self.pillow_image.resize((48, 48))

        self.addButtonImage = ImageTk.PhotoImage(self.pillow_image)

        self.addButton = tk.Label(self.contactListFrame, image=self.addButtonImage)
        self.addButton.bind("<Button-1>", lambda event: self.create_contact_window())
        self.addButton.place(x=386, y=346)

        self.contactListFrame.place(x = 0, y = 36, relheight=1, relwidth=1)

        self.load_contacts()
        self.render_all_contacts()

    #It will render the top part of the app
    def render_top_frame(self):
        #Contact Top Frame
        self.contactTopFrame = tk.Frame(root)
        self.contactTopFrame.rowconfigure(0, weight=0)
        self.contactTopFrame.columnconfigure((0, 1, 2), weight=1)

        #Contact Top Frame Widgets
        tk.Label(self.contactTopFrame, text="Contacts", font="Arial 16").grid(row=0, column=1, sticky="nwse", padx=5, pady=5)

        #Put all frames
        self.contactTopFrame.place(x = 0, y = 0, relheight=0.15, relwidth=1)

    #It will open a window which will allow you to choose to edit or delete contact
    def config_contact(self, event, index):
        self.configContactWindow = tk.Toplevel()
        self.configContactWindow.geometry("340x160")
        self.configContactWindow.title("Config Contact")

        tk.Label(self.configContactWindow, text="What you wanna do with this contact ?", font="Arial 14").pack(fill="both", expand=True)
        tk.Button(self.configContactWindow, text="Edit", command= lambda: self.edit_contact_window(event, index)).pack(side="left", fill="both", expand=True, padx=5, pady=5)
        tk.Button(self.configContactWindow, text="Delete", command= lambda: self.delete_contact(event, index)).pack(side="right", fill="both", expand=True, pady=5, padx=5)
        
        pass

    #Edit the json file it self
    def edit_contact(self, event, index, name, phone):
        self.editContactWindow.destroy()
        self.contactListFrame.destroy()

        with open("contacts.json") as fp:
            data = json.load(fp)
        
        data[index]['name'] = name
        data[index]['phone'] = int(phone)
        
        with open("contacts.json", 'w') as fp:
            json.dump(data, fp)

        self.render_contact_frame()

    #Opens a window similar to create contact, there you can recreate/edit the contact
    def edit_contact_window(self, event, index):
        self.configContactWindow.destroy()

        self.editContactWindow = tk.Toplevel()
        self.editContactWindow.geometry("260x120")
        self.editContactWindow.title("Edit Contact")
        self.editContactWindow.columnconfigure((0, 1), weight=1)
        self.editContactWindow.rowconfigure((0, 1, 2), weight=1)

        tk.Label(self.editContactWindow, text="Name: ", font="Arial 14").grid(column=0, row=0)
        tk.Label(self.editContactWindow, text="Phone: ", font="Arial 14").grid(column=0, row=1)
        name = tk.Entry(self.editContactWindow)
        name.grid(column=1, row=0)
        phone = tk.Entry(self.editContactWindow)
        phone.grid(column=1, row=1)

        tk.Button(self.editContactWindow, text="Edit Contact", command= lambda: self.edit_contact(event, index, name.get(), phone.get())).grid(column=1, row=2, sticky="nswe", padx=5, pady=5)


    #It will delete the indexed contact and rerender the contactListFrame
    def delete_contact(self, event, index):
        self.configContactWindow.destroy()
        self.contactListFrame.destroy()

        with open("contacts.json") as fp:
            data = json.load(fp)
        del data[index]

        with open("contacts.json", 'w') as fp:
            json.dump(data, fp)

        self.render_contact_frame()

    #It loads and stores all contacts in json in the contactList array
    def load_contacts(self):
        if os.path.exists("contacts.json"):
            with open("contacts.json", "r") as f:
                contacts_data = json.load(f)
                self.contactList = [Contact(**data) for data in contacts_data]
                return self.contactList
    
    #It will render each individual contact in a sequence
    def render_all_contacts(self):
        self.imageRaw = []
        self.imageList = []
        self.imageCounter = 0
        def create_image(img, width, height):
            self.imageRaw.append(Image.open(f'{img}'))
            self.imageRaw[self.imageCounter] = self.imageRaw[self.imageCounter].resize((width, height))

            self.imageList.append(ImageTk.PhotoImage(self.imageRaw[self.imageCounter]))

            self.label = tk.Label(self.contactListFrame, image= self.imageList[self.imageCounter])
            self.imageCounter += 1
            return self.label
        
        #Render all contacts
        list = self.contactList
        for i in range(0, len(self.contactList)):
            contactImage = create_image("photoPlaceholder.jpg", 48, 48)
            contactImage.grid(row=i, column=0, sticky="w", padx=5, pady=2)

            contact = tk.Label(self.contactListFrame, text=f"{list[i].name} | {list[i].phone}", font="Arial 12")
            contact.bind("<Button-1>", lambda event, index = i: self.config_contact(event, index))
            contact.grid(row=i, column=1, sticky="nswe")
            
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactList(root)
    root.mainloop()