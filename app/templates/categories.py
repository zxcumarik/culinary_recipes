class Category:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items

    import json

    with open('categories.json', 'r') as file:
        categories = json.load(file)

    print(categories)
