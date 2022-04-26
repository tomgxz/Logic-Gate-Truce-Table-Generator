def _n(a):
    a=int(a)
    return not a
def _a(a,b):
    a=int(a);b=int(b)
    return a and b
def _o(a,b):
    a=int(a);b=int(b)
    return a or b
def _no(a,b):
    a=int(a);b=int(b)
    return n(o(a,b))
def _na(a,b):
    a=int(a);b=int(b)
    return n(a(a,b))
def _xo(a,b):
    a=int(a);b=int(b)
    return a!=b

calls={
    "NOT":"_n",
    "AND":"_a",
    "OR":"_o",
    "NOR":"_no",
    "NAND":"_na",
    "XOR":"_xo",
}


while True:


    i=input("Input the string of values\n\tAn example string would look like this: \"A AND B OR C AND D\"\n\tAny input not in this list: NOT,AND,OR,NOR,NAND,XOR\n\twill be interpereted as a variable to interact with the expression\n\tBrackets are not yet implemented, and it will follow the normal order of presidence\n\tVariables and logic gates are separated with spaces\n\t(Only \"and\", \"or\" and \"not\" work so far)\n\n").upper()

    print()

    path=i.split(" ");variables=[];lines=[];separator="+%+-----+\n"

    for val in path:
        if val not in calls: variables.append(val)

    def genPath(path):
        newPath=path.copy()
        for item in enumerate(path):
            if item[1] in list(calls.values()):
                newPath[item[0]],newPath[item[0]-1]=path[item[0]-1],item[1]
        return newPath

    def genPathNew(path):
        if len(path) == 1: return path

        check=True

        while check:
        
            if path[0] == "NOT":
                t=f"_n({genPathNew(path[1])[0]})"
                path.pop(1)
                path.pop(0)
                path.insert(0,t)

            if len(path)==1: return path
                
            if path[1] == "AND":
                t=f"_a({genPathNew(path[0])},{genPathNew(path[2:])[0]})"
                path.pop(2)
                path.pop(1)
                path.pop(0)
                path.insert(0,t)

            if len(path)==1: return path

            if path[1] == "OR":
                t=f"_o({genPathNew(path[0])},{genPathNew(path[2:])[0]})"
                path.pop(2)
                path.pop(1)
                path.pop(0)
                path.insert(0,t)

            if len(path)==1: return path

            check=False
            
        return path

    path=genPathNew(path)[0]
    
    separator=separator.replace("%","-"*(len(variables)*3+2))

    lines.append("Truce Table\n")
    lines.append(separator)
    lines.append("|%{:>3}{:>3}{:>3}\n".replace("%","{:>3}"*len(variables)).format(*variables,"|","Q","|"))
    lines.append(separator)

    for i in range(2**len(variables)):
        num=str(bin(i)[2:])
        while len(num) < len(variables):num=f"0{num}"
        for j in range(len(variables)):
            exec(f"{variables[j]}=num[{j}]")

        cmd="|%{:>3}{:>3}{:>3}\n"
        cmd=cmd.replace("%","{:>3}"*len(variables))

        cmd=cmd.format(*num,"|",eval(path),"|")
        
        lines.append(cmd)
        lines.append(separator)

    print("".join(lines))
