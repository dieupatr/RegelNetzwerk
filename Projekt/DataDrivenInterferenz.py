



def CountNumFacts(Facts):

       NumberNone=0
       for fact in Facts:
              
              if fact!=None :
                     NumberNone=NumberNone+1
                    
       return NumberNone
                     
def DataDrivenInter(State):

       #Start 

       [A,B,C,D]=State
       Facts=[A,B,C,D]
       
       Num_new=CountNumFacts(Facts)


       while( True ):

              Num_old=Num_new

              #Logic rule based network

              if (A==1) and (B==1):  C=1

              if( C==1) : D=1
       
              ######
       
              #Refresh set of facts
              Facts=  [A,B,C,D]
              Num_new=CountNumFacts(Facts)


              #Check converge
       
              if( Num_new == Num_old) :  break

       return Facts

       


State=[None,None,1,None]

print(DataDrivenInter(State) )
