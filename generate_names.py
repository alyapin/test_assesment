import random
import csv

# Sample lists of names from different nationalities
names = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas",
    "Maria", "Ana", "Antonio", "Francisco", "David", "Miguel", "Manuel", "Jose", "Luis", "Jorge",
    "Yuki", "Sakura", "Takumi", "Haruto", "Aoi", "Sora", "Riko", "Ren", "Hinata", "Kaito",
]

middle_names = [
    "Lee", "Chen", "Wong", "Kim", "Park", "Nguyen", "Tran", "Santos", "Silva", "Garcia",
    "Singh", "Patel", "Kumar", "Lopez", "Gonzalez", "Martinez", "Perez", "Rodriguez", "Fernandez", "Gomez",
    "Ivanov", "Petrov", "Sidorov", "Smirnov", "Popov", "Müller", "Schmidt", "Schneider", "Fischer", "Weber",
]

surnames = [
    "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson",
    "Nguyen", "Tran", "Le", "Pham", "Huynh", "Li", "Wang", "Zhang", "Liu", "Chen",
    "Yamada", "Kobayashi", "Ito", "Sato", "Takahashi", "Watanabe", "Inoue", "Tanaka", "Kato", "Suzuki",
]

# Generate 25 unique combinations of names, middle names, and surnames
data = []
for _ in range(25):
    name = random.choice(names)
    middle_name = random.choice(middle_names)
    surname = random.choice(surnames)
    data.append((name, middle_name, surname))

# Write to CSV file
csv_filename = 'data/names.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['name', 'middle name', 'surname'])
    for row in data:
        csvwriter.writerow(row)

print(f"CSV file '{csv_filename}' generated successfully.")
