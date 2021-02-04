def swap_case(s):
    word_list = list(s)
    new_list = []
    reverse = ''
    for alphabet in word_list:
        if alphabet.islower():
            new_list.append(alphabet.upper())
        elif alphabet.isupper():
            new_list.append(alphabet.lower())
        else:
            new_list.append(alphabet)

    print(word_list)
    print("swapcase", s.swapcase())
    return reverse.join(new_list)


if __name__ == '__main__':
    word = 'Www.HackerRank.com 345'
    print('word: ', word)
    result = swap_case(word)
    print(result)