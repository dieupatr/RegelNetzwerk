
from LexDrawio import *













def ChooseTypOfBlock( typ):

    if typ=="ellipse":  return "ellipse"

    if typ=="shape=or": return "And"

    if typ== "shape=xor": return "Or"

    return None


def FormatInLogic(Value):

    if "<" in Value or ">" in Value or "!" in Value:
        return Value

    if "=" in Value:
        return Value.replace("=","==")



def BuildRuleBasedNetwork(Diagram, DiagramName):

    #Sort blocks
    Blocks= Diagram.blocks

    LogicBlocks={      }

    for block  in Blocks:

        Id=block.Attr['id']
        typ=ChooseTypOfBlock( block.Attr['style'][0] )

        if typ!=None:   LogicBlocks[Id]=[typ ,  block.Attr['value']  ]

        


    #Sort Arrows

    Arrows=Diagram.arrows

    LogicArrwos= {     }

    for arrow in Arrows:

        source=arrow.Attr['source']
        target=arrow.Attr['target']
        LogicArrwos[source]=target


    



    #################################

    
    File=open(DiagramName+".py",'w')

    #Build Preload
    



    #Build Simpel Rules

    for key in LogicArrwos:

        source=key
        target=LogicArrwos[key]

        TargetBlock=LogicBlocks[target]
        SourceBlock=LogicBlocks[source]
        
        TypTargetBlock=TargetBlock[0]

        if  TypTargetBlock=="And" or TypTargetBlock=="Or": continue


        Value=FormatInLogic(SourceBlock[1])

        Rule=f"\tif ({Value}): { TargetBlock[1]}\n"

        File.write(Rule)


    # Build cojugation ( and , or  )
    
    for  keyblock in LogicBlocks:

        Typ=LogicBlocks[keyblock][0]

        #Find chuild blocks

        if Typ=="And" or Typ=="Or":

            Id=keyblock

            ChildBlocks=[  ]

            for keyarrow in LogicArrwos:

                target=LogicArrwos[keyarrow]
                
                if target==keyblock:  ChildBlocks.append(keyarrow)

        #Build Rule

            N=len(ChildBlocks)

            Rule="if "

            Quantor="and"  if Typ=="And" else "or"

            for k in range(N-1):

                Value=FormatInLogic(LogicBlocks[ChildBlocks[k]][1])

                Rule=Rule+"( "+Value+")"+ Quantor

            Rule=Rule+" ("+FormatInLogic(LogicBlocks[ChildBlocks[N-1]][1])+" ) : "+LogicBlocks[keyblock][1]+"\n"

            File.write(Rule)

        else:
            continue


        


    File.close()
        

        



    



    



    







file_path = 'TestRunDia.drawio'  

Dia=ParseDiagramsFromXmlFile(file_path)

Dia=Dia["Test1"]

BuildRuleBasedNetwork(Dia,"Test1")


    
    




