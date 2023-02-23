def main():
    string = input("Enter a string: ")
    resault = 0
    bol = True
    for i in range(0, len(string)):
        if string[i:].startswith("on") or string[i:].startswith("ON"):
            bol = True
        elif string[i:].startswith("off") or string[i:].startswith("OFF"):
            bol = False
        elif string[i].isdigit() and bol:
            resault += int(string[i])
        elif string[i]=="=":
            print(resault)
            resault = 0
    
if __name__ == "__main__":
    main()