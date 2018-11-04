class Scanner:

    def __init__(self, s):
        self.stream = []
        self.loc = s
        AZ = [chr(ord('A')+i) for i in range(26)]
        file = open(s, "r")
        for line in file:
            l = line.strip().split()
            i = 0
            while i < len(l):
                token = l[i]
                if token.upper() == "IF":
                    self.stream.append(("IF", 0))
                elif token.upper() == "GOTO":
                    self.stream.append(("GOTO", 0))
                elif token.upper() == "PRINT":
                    self.stream.append(("PRINT", 0))
                elif token.upper() == "STOP":
                    self.stream.append(("STOP", 0))
                elif token == "+":
                    self.stream.append(("+", 1))
                elif token == "-":
                    self.stream.append(("-", 2))
                elif token == "<":
                    self.stream.append(("<", 3))
                elif token == "=":
                    self.stream.append(("=", 4))
                elif token.upper() in AZ:
                    self.stream.append(("id", ord(token.upper()) - ord('A')))
                else:
                    self.stream.append(("number", int(token)))
                i += 1
        file.close()
        self.stream.append(("EOF", 0))

    def getStream(self):
        return self.stream
