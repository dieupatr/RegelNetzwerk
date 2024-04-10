

def CountNumFacts(Facts):

       NumberNone=0
       for fact in Facts:
              
              if fact!=None :
                     NumberNone=NumberNone+1
                    
       return NumberNone 
    
def DataDrivenInter_Test1(State):
               
       #Start 

       [A,B,C,D,E]=State
       Facts=[A,B,C,D,E]
       Num_new=CountNumFacts(Facts) 

       while( True ):

              Num_old=Num_new

              #Logic rule based network

              
              if (C==1): D=1


              if (    A > j jjj) or ( B==1) or  (E==1 ) : C=1




             #Refresh set of facts
              Facts= [A,B,C,D,E]
              Num_new=CountNumFacts(Facts)


              #Check converge
       
              if( Num_new == Num_old) :  break

       return Facts

[A,B,C,D,E]=[None,None,None,None,None]
State=[A,B,C,D,E]
print(DataDrivenInter_Test1(State))
    