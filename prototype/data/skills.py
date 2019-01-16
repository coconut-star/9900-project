#!/usr/bin/python3
import csv

with open('skills.csv', 'r') as input:
    reader = csv.reader(input)
    skills = list(reader)
    output = open('skills.sql', 'w')
    # Skip header
    for line in range(1, len(skills)):
        skill = skills[line]
        print(skill)
        if len(skill) != 4:
            print('ERROR: line {} is incomplete'.format(i + 1))
            exit(1)
        category = skill[0].strip()
        if str.lower(category) == 'root':
            category = 'null'
        else:
            category = '''(select id from backend_skill where name='{}' and type='C')'''.format(category)
        name = skill[1].strip()
        desc = skill[2].strip()
        s_type = str.upper(skill[3].strip()[0])
        print('''INSERT INTO backend_skill (name, description, type, category_id) VALUES ('{}','{}','{}',{});'''.format(name, desc, s_type, category), file=output)
    output.close()
