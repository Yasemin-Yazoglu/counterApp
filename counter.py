import tkinter as tk
import json

class CounterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Counter App")

        self.counters = {}

        self.create_widgets()


    def create_widgets(self):
        # Label and entry for counter name
        self.name_label = tk.Label(self.master, text="Enter Counter Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Label and Entry for target count
        self.target_label = tk.Label(self.master, text="Set Target Count:")
        self.target_label.grid(row=1, column=0, padx=10, pady=5)
        self.target_entry = tk.Entry(self.master)
        self.target_entry.grid(row=1, column=1, padx=10, pady=5)

        # Button to create counter
        self.create_button = tk.Button(self.master, text="Create Counter", command=self.create_counter)
        self.create_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Listbox to display counters
        self.counter_listbox = tk.Listbox(self.master, width=40)
        self.counter_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
      
        # Button to delete counters
        self.delete_button = tk.Button(self.master, text="Delete Counter", command=self.delete_counter)
        self.delete_button.grid(row=4, column=0, padx=10, pady=5)

        # Button to reset the counter
        self.reset_button = tk.Button(self.master, text="Reset Counter", command=self.reset_counter)
        self.reset_button.grid(row=4, column=1, padx=10, pady=5)

        # Space bar to increment counter
        self.master.bind('<space>', self.increment_counter)

    def create_counter(self):
        counter_name = self.name_entry.get()
        target_count = int(self.target_entry.get())

        self.counters[counter_name] = {
            'count': 0,
            'target': target_count
        }

        self.update_listbox()

    def increment_counter(self, event):
        focused_widget = self.master.focus_get()
        if focused_widget == self.counter_listbox:
            selected_item_index = self.counter_listbox.nearest(event.y_root - self.counter_listbox.winfo_rooty())
            if selected_item_index >= 0:
                counter_name = self.counter_listbox.get(selected_item_index)
                counter_name = counter_name.split(':')[0].strip()

                if counter_name in self.counters:
                    if self.counters[counter_name]['count'] < self.counters[counter_name]['target']:
                        self.counters[counter_name]['count'] += 1
                        self.update_listbox()
    
    def delete_counter(self):
        selected_index = self.counter_listbox.curselection()
        if selected_index:
            counter_name = self.counter_listbox.get(selected_index)
            counter_name = counter_name.split(':')[0].strip()

            if counter_name in self.counters:
                del self.counters[counter_name]
                self.update_listbox()

    def reset_counter(self):
        selected_index = self.counter_listbox.curselection()
        if selected_index:
            counter_name = self.counter_listbox.get(selected_index)
            counter_name = counter_name.split(':')[0].strip()

            if counter_name in self.counters:
                self.counters[counter_name]['count'] = 0
                self.update_listbox()


    def update_listbox(self):
        self.counter_listbox.delete(0, tk.END)
        for counter_name, counter_data in self.counters.items():
            self.counter_listbox.insert(tk.END, f"{counter_name}: {counter_data['count']}/{counter_data['target']}")

    def save_data(self):
        with open("counters.json", "w") as f:
            json.dump(self.counters, f)

    def load_data(self):
        try:
            with open("counters.json", "r") as f:
                self.counters = json.load(f)
                self.update_listbox()
        except FileNotFoundError:
            pass

    def run(self):
        self.load_data()
        self.master.mainloop()
        self.save_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = CounterApp(root)
    app.run()
