import csv
import json
import os

class Database:
    def __init__(self, keys):
        self.contents = []
        self.keys = keys  # List of keys, e.g., ['age', 'salary']

    def add(self, itemname, *args):
        if len(args) > len(self.keys):
            raise ValueError("Too many arguments passed for the defined keys.")

        item = {"name": itemname}
        for key, value in zip(self.keys, args):
            item[key] = value

        self.contents.append(item)

    def bulk_add(self, items):
        for itemname, *args in items:
            self.add(itemname, *args)

    def remove(self, no):
        if 0 <= no < len(self.contents):
            removed = self.contents.pop(no)
            print(f"Removed entry at index {no}: {removed}")
        else:
            print(f"Index {no} out of range. Nothing removed.")

    def update(self, no, **kwargs):
        if 0 <= no < len(self.contents):
            for key, value in kwargs.items():
                if key in self.keys or key == "name":
                    self.contents[no][key] = value
            print(f"Updated entry at index {no}: {self.contents[no]}")
        else:
            print(f"Index {no} out of range. Nothing updated.")

    def sort_by(self, key, reverse=False):
        if key not in self.keys and key != "name":
            print(f"Cannot sort by unknown key: {key}")
            return
        self.contents.sort(key=lambda item: item.get(key, None), reverse=reverse)

    def count(self):
        return len(self.contents)

    def average(self, key):
        values = [item.get(key) for item in self.contents if isinstance(item.get(key), (int, float))]
        return sum(values) / len(values) if values else 0

    def find_partial(self, key, substring):
        results = []
        for i, entry in enumerate(self.contents):
            val = entry.get(key, "")
            if substring.lower() in str(val).lower():
                results.append((i, entry))
        return results

    def export_csv(self, filename):
        os.makedirs('Exports', exist_ok=True)
        filepath = os.path.join('Exports', filename)
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Index", "name"] + self.keys)
            for i, item in enumerate(self.contents):
                row = [i, item.get("name")] + [item.get(k, "") for k in self.keys]
                writer.writerow(row)
        print(f"Exported database to {filepath}")

    def export_json(self, filename):
        os.makedirs('Exports', exist_ok=True)
        filepath = os.path.join('Exports', filename)
        with open(filepath, 'w') as f:
            json.dump(self.contents, f, indent=4)
        print(f"Exported database to {filepath}")

    def import_json(self, filename):
        filepath = os.path.join('Exports', filename)
        if not os.path.exists(filepath):
            print(f"File {filepath} does not exist. Import failed.")
            return
        with open(filepath, 'r') as f:
            self.contents = json.load(f)
        print(f"Imported database from {filepath}")

    def __str__(self):
        length = len(self.contents)
        entries = "\n".join(f"{i}. {entry}" for i, entry in enumerate(self.contents))
        return f"The database is {length} long.\nContents:\n{entries}"

sys.path.append("C:/Users/GOD IS LOVE/Documents/Calvin files/Projects/pydb/pydb")
