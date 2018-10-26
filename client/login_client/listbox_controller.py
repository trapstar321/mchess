from tkinter import END


class ListBoxController:
    def __init__(self, data, listbox):
        self.data = data
        self.listbox = listbox

    def clear(self):
        self.data = {}
        self.listbox.delete(0, END)

    def get_selected(self):
        if len(self.listbox.curselection()) == 0:
            return None

        index = int(self.listbox.curselection()[0])

        for id_ in self.data.keys():
            if self.data[id_].index == index:
                return self.data[id_]

    def add(self, item):
        item.set_index(self.listbox.size())
        self.data[item.get_key()] = item
        self.listbox.insert(END, item)

    def delete(self, key_):
        value = self.data[key_]
        self.listbox.delete(value.index)
        del self.data[key_]

        for key_ in self.data.keys():
            self.data[key_].index = self.listbox.get(0, "end").index(
                str(self.data[key_]))


