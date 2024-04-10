from LexDrawio import *
import sys





def DectectError(value,pattern):

       match=re.findall(pattern, value)
       
       

       if len(match)>0:
              print(f"Error in : {value} ")
              sys.exit(0)

       else:
              pass


def CheckSyntax( value,pattern):

    pattern = re.compile(pattern)
    if pattern.match(value):
        pass
       
    else:
           
           print(f"Syntax Error in : {value} '")
           sys.exit(0)








def GenerateCode(ConjugateRules,SimpelRules,Literals,StateLiterals,DiagramName):

    return f"""

def CountNumFacts(Facts):

       NumberNone=0
       for fact in Facts:
              
              if fact!=None :
                     NumberNone=NumberNone+1
                    
       return NumberNone 
    
def RuleNetwork_{DiagramName}(State):
               
       #Start 

       {Literals}=State
       Facts={Literals}
       Num_new=CountNumFacts(Facts) 

       while( True ):

              Num_old=Num_new

              #Logic rule based network

              
{SimpelRules}

{ConjugateRules}



             #Refresh set of facts
              Facts= {Literals}
              Num_new=CountNumFacts(Facts)


              #Check converge
       
              if( Num_new == Num_old) :  break

       return Facts

# State:      {Literals}={StateLiterals}     

    """



def WhiteSpace(Nspace):
    space=""
    for k in range(Nspace): space=space+" "

    return space


def ChooseTypOfBlock( typ):

    if typ=="ellipse":  return "ellipse"

    if typ=="shape=or": return "And"

    if typ== "shape=xor": return "Or"

    return None


def FormatInLogic(Value):

    DectectError(Value,r'[^a-zA-Z0-9\s_\"<>!=]')

    CheckSyntax( Value,r'\s*[a-zA-Z0-9_]*\s*[=<>!]*\s*[a-zA-Z0-9_\"]*$')

    if "<" in Value or ">" in Value or "!" in Value:
        return Value

    if "=" in Value:
        return Value.replace("=","==")


def ParseDiagram(Diagram):

    
    Blocks= Diagram.blocks
    Arrows=Diagram.arrows

    # find list's
    SetWithLists={ }

    for block in Blocks:
        Id=block.Attr['id']
        typ=block.Attr['style'][0]
        
        if typ=="swimlane" : SetWithLists[Id]=[   ]
    

    # Link Labels
    
    for block in Blocks:

        Id=block.Attr['id']
        typ=block.Attr['style'][0]
        parent=block.Attr['parent']

        if typ=="text" : 
            try:
                SetWithLists[parent].append(block.Attr['value'])
            except:
                pass
    
    Variables=[ ]
    for KeyList in  SetWithLists:  Variables.extend(SetWithLists[KeyList])
    StateLiterals=["None" for k in range(len(Variables))]


    Literals="["+','.join(Variables)+"]"
    StateLiterals="["+','.join(StateLiterals)+"]"


      #Sort blocks          
    
    LogicBlocks={      }

    for block  in Blocks:

        Id=block.Attr['id']
        typ=ChooseTypOfBlock( block.Attr['style'][0] )

        if typ!=None:   LogicBlocks[Id]=[typ ,  block.Attr['value']  ]

    #Sort Arrows


    LogicArrwos= {     }

    for arrow in Arrows:

        source=arrow.Attr['source']
        target=arrow.Attr['target']
        LogicArrwos[source]=target


    
    #################################
    
    #Build Simpel Rules
        
    SimpelRules=""

    for key in LogicArrwos:

        source=key
        target=LogicArrwos[key]

        TargetBlock=LogicBlocks[target]
        SourceBlock=LogicBlocks[source]
        
        TypTargetBlock=TargetBlock[0]

        if  TypTargetBlock=="And" or TypTargetBlock=="Or": continue


        Value=FormatInLogic(SourceBlock[1])

        Rule=f"{WhiteSpace(14)}if ({Value}): { TargetBlock[1]}\n"

        SimpelRules=SimpelRules+Rule


    # Build cojugation ( and , or  )
    
    ConjugateRules=""
    
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

            Rule=f"{WhiteSpace(14)}if "

            Quantor=" and "  if Typ=="And" else " or "

            for k in range(N-1):

                Value=FormatInLogic(LogicBlocks[ChildBlocks[k]][1])

                Rule=Rule+"( "+Value+")"+ Quantor

            Rule=Rule+" ("+FormatInLogic(LogicBlocks[ChildBlocks[N-1]][1])+" ) : "+LogicBlocks[keyblock][1]+"\n"

            ConjugateRules=ConjugateRules+Rule

        else:
            continue

    return [ConjugateRules,SimpelRules,Literals,StateLiterals]
        

        



def BuildRuleBasedNetwork(file_path, TabName):

    Dia=ParseDiagramsFromXmlFile(file_path)
    Dia=Dia[TabName]
    
    [ConjugateRules,SimpelRules,Literals,StateLiterals]=ParseDiagram(Dia)

    Code=GenerateCode(ConjugateRules,SimpelRules,Literals,StateLiterals,TabName)

    #Write in File
    
    File=open(TabName+".py","w")
    Code=re.sub(r'[^\x00-\x7F]+', '', Code)
    File.write(Code)
    File.close()
    



### Main

file_path =sys.argv[1]
  
TabName=sys.argv[2]



BuildRuleBasedNetwork(file_path,TabName)




###########




    
    




