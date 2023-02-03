


FILENAME_SRC = 'slovnik_full.txt'
FILENAME_OUT = 'slovnik5.txt'



def main():

    words, lines = 0, 0

    with open(FILENAME_OUT, 'w', encoding='UTF-8') as file_out, open(FILENAME_SRC, 'r', encoding='UTF-8') as file_src:
        for line in file_src:
            word = line.strip()
            if len(word) == 5 and word[0].upper() != word[0]:
                words += 1
                file_out.write(word+'\n')
            lines += 1

    print(f'lines: {lines}, words: {words}')


main()