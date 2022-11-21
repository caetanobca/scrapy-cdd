text_file = open("lista_deputadas_string_list_txt.txt", "r")
text_file = text_file.read().replace('"', '')
lines = text_file.split(',\n')

print((lines))