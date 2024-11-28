



def creation_id(chaine):
    letters = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','z']
    value_word = 0
    id_letters = []
    mots = dict()

    for i in range(len(letters)):
        id_letters.append(i)
    for i in chaine:
        for j in letters:
            if j == i and j != ' ':
                value_word += id_letters[letters.index(i)]
    return str(value_word)
