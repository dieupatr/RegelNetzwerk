
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

        LogicBlocks[Id]=[typ ,  block.Attr['value']  ]


    #Sort Arrows

    Arrows=Diagram.arrows

    LogicArrwos= {     }

    for arrow in Arrows:

        source=arrow.Attr['source']
        target=arrow.Attr['target']
        LogicArrwos[source]=target



    #################################

    #Build Simpel Rules
    File=open(DiagramName+".py",'w')

    for key in LogicArrwos:

        source=key
        target=LogicArrwos[key]

        TargetBlock=LogicBlocks[target]
        SourceBlock=LogicBlocks[source]
        
        TypTargetBlock=TargetBlock[0]

        if  TypTargetBlock=="And" or TypTargetBlock=="Or": continue


        Value=FormatInLogic(SourceBlock[1])

        Rule=f"if ({Value}): { TargetBlock[1]}\n"

        File.write(Rule)



    for  key in LogicBlocks:

        Typ=LogicBlocks[key][0]

        if Typ=="And" or Typ=="Or":

            Id=key
            
            pass
        
        else:
            continue


        


    File.close()
        

        



    



    



    







file_path = 'TestRunDia.drawio'  

Dia=ParseDiagramsFromXmlFile(file_path)

Dia=Dia["Test1"]

BuildRuleBasedNetwork(Dia,"Test1")


    
    




