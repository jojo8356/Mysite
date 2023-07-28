def get_doc(Class):
    liste = []
    name = Class.__name__
    name = name.lower()
    try:
        liste = open("doc.txt","r").readlines()
    except:
        liste = []
    test = False
    for x in liste:
        if Class.__name__ in x:
            test = True
            break
    liste = []
    try:
        code = open(f"{name}.py").read().split("\n")
    except:
        print(f"{name}.py qui a la class {Class.__name__}")
    for x in code:
        if "class" in x:
            index = code.index(x)
            break
    code = code[index:]
    for x in code:
        if "class" in x:
            liste.append(x)
        elif "__" in x:
            pass
        elif "def" in x:
            liste.append("    " + x)
        elif x.count('"""') == 2:
            liste.append("    " + x)
    for x in liste:
        index = liste.index(x)
        if '"""' in liste[index]:
            liste[index-1] += " " + liste[index].replace("    ", "") + "\n"
            del liste[index]
    for x in liste:
        index = liste.index(x)
        liste[index] = liste[index].replace('"""', "").replace("def ", "").replace("class ", "").replace("self,", "").replace("self", "").replace("self, ", "").replace("self , ", "")
    liste2 = liste[1:]
    liste2.sort()
    liste = [liste[0]]
    for x in liste2:
        liste.append(x)
    if test:
        return
    else:
        doc = ("\n".join(liste)) + "\n"
        if Class.__name__ == "Model":
            with open("doc.txt", "w") as file:
                file.write(doc)
        else:
            with open("doc.txt", "a") as file:
                file.write(doc)

