import json

import rstr

# with open('my_intent_catcher_data/train.json', encoding="utf-8") as f:
with open('supporting_train.json', encoding="utf-8") as f:
    templates = json.load(f)

for section, commands in templates.items():
    print(section)
    commands = '\n'.join(commands)
    commands = commands.split('\n')

    i = 0
    while i < len(commands):
        a = []
        reg = commands[i]
        j = 0
        while j < 1000:
            s = rstr.xeger(reg)
            if a.count(s) == 0:
                a.append(s)
            j += 1
        j = 0
        while j < len(a):
            print("\"" + a[j].strip() + "\",")
            j += 1
        i += 1
    print('\n\n')

# reg = "выдать список ((ссылок)){0,1}"
# a = []
# s = ''
# i = 0
# while i < 1000:
#     s = rstr.xeger(reg)
#     if a.count(s) == 0:
#         a.append(s)
#     i += 1
#
# i = 0
# while i < len(a):
#     print("\"" + a[i].strip() + "\",")
#     i += 1
