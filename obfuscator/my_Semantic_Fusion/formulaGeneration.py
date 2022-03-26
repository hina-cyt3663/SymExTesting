import random
import math

"""
has not support generate formula by adding two quadratic formula
"""
formulaResultPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/formatRecipe/formulas"
formulaResultFile=open(formulaResultPath,"w+")

def solveQuadratic(a,b,c):
    delta=b*b-4*a*c
    if(delta<0):
        return ("quad0",a,b,c)
    elif(delta>0):
        solution1=(-b-math.sqrt(delta))/2*a
        solution2=(-b+math.sqrt(delta))/2*a
        return("quad1",a,b,c,solution1,solution2)

def generateFormula(formula1,formula2):
    SATFormulas=[]
    UNSATFormulas=[]
    if(formula1[0]=="linear" and formula2[0]=="linear"):
        template="{a1}*#+{b1}{sym1}{c1} & {a2}*#+{b2}{sym2}{c2},{SAT}\n"
        solution1=formula1[4]
        solution2=formula2[4]
        if(solution1>solution2):
            UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT="UNSAT"))
            SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2=">",SAT="SAT"))
        elif(solution1<solution2):
            SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT="SAT"))
            UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2=">",SAT="UNSAT"))
    
    if(formula1[0]=="linear" and formula2[0][0]=="q"):
        template="{a1}*#+{b1}{sym1}{c1} & {a2}*#*#+{b2}*#+{c2}{sym2}0,{SAT}\n"
        if(formula2[0]=="quad0"):
            UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT="UNSAT"))
            SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2=">",SAT="SAT"))
        if(formula2[0]=="quad1"):
            solution=formula1[-1]
            solution1=formula2[-2]
            solution2=formula2[-1]
            if(solution<solution1):
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2=">",SAT="SAT"))
                UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2="<",SAT="UNSAT"))
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT="SAT"))
            elif(solution>solution2):
                UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2=">",SAT="UNSAT"))
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2=">",SAT="SAT"))
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2="<",SAT="SAT"))
            else:
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT="SAT"))
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2=">",SAT="SAT"))
    if(formula1[0][0]=="q" and formula2[0]=="linear"):
        SATFormulas,UNSATFormulas=generateFormula(formula2,formula1)
    return SATFormulas,UNSATFormulas

def main():
    linearFormulas=[]
    for i in range(20):
        a=abs(round(random.random(),2))
        if(a==0):
            continue
        b=round(random.random(),2)
        c=round(random.random(),2)
        solution=(c-b)/a
        linearFormulas.append(("linear",a,b,c,solution))
    
    quadFormulas=[]
    for i in range(20):
        a=abs(round(random.random(),2))
        if(a==0):
            continue
        b=round(random.random(),2)
        c=round(random.random(),2)
        formula=solveQuadratic(a,b,c)
        quadFormulas.append(formula)
    for i in range(2):
        form1,form2=random.sample(linearFormulas,2)
        result=generateFormula(form1,form2)
        for item in result:
            formulaResultFile.writelines(item)
    for i in range(2):
        form1=random.choice(linearFormulas)
        form2=random.choice(quadFormulas)
        result=generateFormula(form1,form2)
        for item in result:
            formulaResultFile.writelines(item)
    formulaResultFile.close()
main()


