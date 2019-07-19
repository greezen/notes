import json
import csv

data = [{'name': '张三', 'age': 20, 'male': True}, {'name': 'lisi', 'age': 20, 'male': False}]

with open('t.json', 'w') as f:
    json.dump(data, f)

with open('t.json', 'r') as f:
    jf = json.load(f)
    print(jf)

with open('t.csv', 'w') as f:
    print(id(f))
    writer = csv.DictWriter(f, ['name', 'age', 'male'])
    writer.writeheader()
    writer.writerows(data)

with open('t.csv', 'r') as f:
    print("%x"%id(f))
    reader = csv.DictReader(f)
    for row in reader:
        print(row, row['name'], row['age'], row['male'])