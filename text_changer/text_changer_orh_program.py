with open('CTV 18 00 30 iuni.txt', 'r', encoding='utf-8') as inp_file:
    inp_text = inp_file.read()

inp_strings = inp_text.split('\n')

checker1 = 0
checker2 = 0
new_text = ''

for string in inp_strings:

    string = string.replace(inp_strings[0].replace('﻿', ''), '')

    if string.find('GENERIC OUT') != -1:
        break
    if string.find('Длительность планируемая:') != -1 or string.find('Длительность фактическая:') != -1 or string.find('00:00:00:00') != -1 or string.find('Дата планируемого эфира:') != -1 or string.find('Автор: ') != -1 or string.find('Bumper BETA') != -1:
        continue
    stop = 0
    for i, symb in enumerate(string):
        if i + 3 <= len(string):
            if symb.isnumeric() and (string[i+1] == '.' or string[i+1] == '/') and string[i+2].isnumeric():
                stop = 1
    if stop == 1:
        continue
    new_text += string+' '
new_text2 = ''
for string in new_text.split('№'):
    string = '№'+string
    new_text2 += string + '\n'
new_text = ''

for i, string in enumerate(new_text2.split('\n')):
    if (string.find('№2') != -1 or checker2 != 0) and string.find('.VW ') == -1:
        checker2 += 1
        if len(new_text2.split('\n')) > i+1:
            if new_text2.split('\n')[i+1][:new_text2.split('\n')[i+1].find('.')] != string[:string.find('.')]:
                new_text += '  ' + string + '\n'
            elif len(new_text2.split('\n')[i+1]) < len(string):
                new_text += '  ' + string + '\n'
            else:
                continue
        else:
            new_text += '  ' + string + '\n'

new_text2 = ''
checker = 0
skip = False

for i, string in enumerate(new_text.split('\n')):
    if skip == True:
        skip = False
        continue
    if i > 0 and len(new_text.split('\n')) > i + 1:
        changed_string0 = string.upper().replace('ИНТРО', 'INTRO').replace('интро', 'INTRO')
        changed_string1 = new_text.split('\n')[i+1].upper().replace('БЕТА', 'BETA').replace('бета', 'BETA')
        if changed_string0.find('INTRO') != changed_string0.rfind('INTRO') and changed_string1.find('BETA') != changed_string1.rfind('BETA'):
            string = string + ' ' + new_text.split('\n')[i+1][changed_string1.rfind('BETA') + 4:]
            skip = True
    new_text2 += string + '\n\n'

with open('orh_out.txt', 'w', encoding='utf-8') as out_file:
    out_file.write(new_text2)
