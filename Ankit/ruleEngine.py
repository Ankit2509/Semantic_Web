# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 00:14:57 2019

@author: ankit
"""


from neo4j import GraphDatabase
import json
#import urllib.request
#with urllib.request.urlopen("http://81dbfa16.ngrok.io/login.php") as url:
#   data = json.loads(url.read().decode())

#from neo4j import GraphDatabase
#import urllib.request, json 
#with urllib.request.urlopen("http://81dbfa16.ngrok.io/login.php") as url:
#    data = json.loads(url.read().decode())
def serch(list,index,value):
    for n in range(index-1,-1,-1):
        if(list[n]==value):
            return(n)
    return "a"

def Initial():
    actors=[]
    directors=[]
    movie=[]
    predicates=[]

    uri="bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "1234"))
    db=driver.session()

    # print(db)

    res=db.run("match(n:ns1__Actors) return n.uri")
    for record in res:
        s1=record["n.uri"]
        s2="#"
        actors.append(s1[s1.index(s2) + len(s2):])

    res=db.run("match(n:ns1__Director) return n.uri")
    for record in res:
        s1=record["n.uri"]
        s2="#"
        directors.append(s1[s1.index(s2) + len(s2):])


    res=db.run("match(n:ns1__Movie) return n.uri")
    for record in res:
        s1=record["n.uri"]
        s2="#"
        movie.append(s1[s1.index(s2) + len(s2):])


    res=db.run("match(n:owl__ObjectProperty) return n.rdfs__label as asd")
    for record in res:
        # s1=record["n.rdfs__label"]
        # s2="#"
        predicates.append(record["asd"])

    db.close()
    print(actors,directors,predicates,movie)
    return(actors,directors,predicates,movie)

def Main(data):
    print("gotcha")
    
    # data={"rule":"Inverse"}
    # prop=data["rule"]
        
    uri="bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "1234"))
    db=driver.session()

    # data={"items":[{"subject":"Tabu","predicate":"Acted_In","object":"?movie","connector":"AND"},{"subject":"Akshay_Kumar","predicate":"Acted_In","object":"?movie","connector":"OR"},{"subject":"Amit_Sharma","predicate":"isDirectorOf","object":"?movie","connector":"AND"},{"subject":"?director","predicate":"isDirectorOf","object":"Andhadhun","connector":"THEN"},{"subject":"?movie","predicate":"willHaveRating","object":"Low","connector":"0"}]}

    condition=[]
    temp=[]
    variables=[]

    print(data, type(data))

    for n in range(len(data["items"])):
        temp=[]
        if (data["items"][n]["subject"][0]=='?'):
           temp.append("sub")
           variables.append(data["items"][n]["subject"])
        else:
            temp.append(data["items"][n]["subject"])
            
        temp.append(data["items"][n]["predicate"])
        if (data["items"][n]["object"][0]=='?'):
           temp.append("obj")
           variables.append(data["items"][n]["object"])
        else:
            temp.append(data["items"][n]["object"])
            
        temp.append(data["items"][n]["connector"])
        if ((data["items"][n]["subject"][0]!='?') and (data["items"][n]["object"][0]!='?')):
            variables.append(" ")
        
        condition.append(temp)
          
    print(variables)



    index=[]
    temp=0

    for i in range(len(variables)-1):
        if(variables[i]!=variables[i+1]):
            index.append(i)
    print(index)



    sets=[set() for _ in range(len(index))]











    m=len(data["items"])
    query=""
    flag=0
    lst=[]
    for n in range(m-1):
        flag=0
        mst=[]
        if(condition[n][0]=="sub"):
            #subject is a variable
            pred=condition[n][1]
            obj=condition[n][2]
            a=chr(ord('a') + n)
            query1=" match("+a+"1)-["+a+"2:ns1__"+pred+"]->("+a+"3:owl__NamedIndividual{uri:'http://www.iiitb.ac.in/MovieOntology#"+obj+"'}) return  "+a+"1.uri as subject "
            result=db.run(query1)
            for record in result:
                mst.append(record["subject"])
            lst.append(mst)
        else:
            sub=condition[n][0]
            pred=condition[n][1]
            a=chr(ord('a') + n)
            query1=" match("+a+"1:owl__NamedIndividual{uri:'http://www.iiitb.ac.in/MovieOntology#"+sub+"'})-["+a+"2:ns1__"+pred+"]->("+a+"3) return  "+a+"3.uri as object "
            result=db.run(query1)
            for record in result:
                mst.append(record["object"])
            lst.append(mst)
            

    print(lst)

    '''shardul''' #variables
    print("*"*10)
    print(condition)
    set_operations = []
    for cond in condition:
        set_operations.append(cond[3])
    print(set_operations)

    n = len(variables)

    res = {}
    set_curr = ()
    for i in range(0, (n-1)):
        var_curr = variables[i]
        set_curr = set(lst[i])
        if(var_curr not in res):
            res[var_curr] = set_curr
            continue
        #set_prev = res[var_curr]
        if(set_operations[i-1]=="OR"):
            res[var_curr] = res[var_curr].union(set_curr)
        elif(set_operations[i-1]=="AND"):
            res[var_curr] = res[var_curr].intersection(set_curr)
        #print(i, var_curr, set_operations[i-1], res)

    print(res)
    print("*"*10)
    '''/shardul'''


    sub=condition[m-1][0]  
    pred=condition[m-1][1]
    obj=condition[m-1][2]

    subject=[]
    predicate=[]
    objecti=[]
    if(condition[m-1][0]=="sub"):
        vary=variables[len(variables)-1]
        lst=res[vary]
        
        for subj in lst:
            query=" MATCH (a3:owl__NamedIndividual{uri:'http://www.iiitb.ac.in/MovieOntology#"+obj+"'}) MATCH (a1:owl__NamedIndividual{uri:'"+subj+"'}) MERGE (a1)-[a2:ns1__"+pred+"]->(a3) return a1.uri as subject,'"+pred+"' as predicate,a3.uri as object"
            results=db.run(query)
            #print(query)
            for records in results:
                #print(records)
                subject.append(records["subject"])
                predicate.append(records["predicate"])
                objecti.append(records["object"])
                #print(subject)
        
    else:
        vary=variables[len(variables)-1]
        print("check")
        print(sub)

        lst=res[vary]
        for obje in lst:
            query=" MATCH (a3:owl__NamedIndividual{uri:'"+obje+"'}) MATCH (a1:owl__NamedIndividual{uri:'http://www.iiitb.ac.in/MovieOntology#"+sub+"'}) MERGE (a1)-[a2:ns1__"+pred+"]->(a3) return a1.uri as subject,'"+pred+"' as predicate,a3.uri as object"
            result=db.run(query)
            print(query)
            for record in result:
                subject.append(record["subject"])
                print(subject)
                predicate.append(record["predicate"])
                objecti.append(record["object"])

        
    print(subject,predicate,objecti)

    db.close()

    return(subject, predicate, objecti)