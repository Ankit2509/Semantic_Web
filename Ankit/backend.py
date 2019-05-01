
from neo4j import GraphDatabase
import json
#import urllib.request
#with urllib.request.urlopen("http://81dbfa16.ngrok.io/login.php") as url:
#   data = json.loads(url.read().decode())

def Main(prop):
    # data={"rule":"Transitivity"}
    # prop=data["rule"]
      
	uri="bolt://localhost:7687"
	driver = GraphDatabase.driver(uri, auth=("neo4j", "1234"))
	db=driver.session()
	uri="match(n:owl__Ontology) return n.uri as uri"
	Properties="match(n:owl__ObjectProperty) return n.rdfs__label as rdfs__label,n.uri as uri"


	


	if(prop=="Transitivity"):
		property_label=[]
		property_uri=[]
		i=0
		uri=db.run(uri)
		for record in uri:
		    uri=record["uri"]
		    print(uri)
		result=db.run(Properties)
		for record1 in result:
		    property_label.insert(i,record1["rdfs__label"])
		    property_uri.insert(i,record1["uri"])
		    i=i+1
		# print(property_label)

		sub=[]
		pred=[]
		obj=[]
		for properties in property_label:
		    data=db.run("match(n1)-[:ns1__"+properties+"]->(n2)-[:ns1__"+properties+"]->(n3) merge(n1)-[r:ns1__"+properties+"]->(n3) return n1.uri as subject,r as predicate,n3.uri as object ")
		    for record in data:
		        sub.append(record["subject"])
		        pred.append(properties)
		        obj.append(record["object"])

		data={}
		js=[]
		dictn={}
		data["subject"]=sub
		data["predicate"]=pred
		data["object"]=obj
		js.append(data)
		dictn["res"]=js
		#print(json.dumps(dictn))

		db.close()
		return dictn
    # print(sub)


	if(prop=="Inverse"):

	    
	    uri=db.run(uri)
	    for record in uri:
	        uri=record["uri"]
	        # print(uri)
	    result=db.run("match(n1:owl__ObjectProperty)-[:owl__inverseOf]->(n2:owl__ObjectProperty) return n1.rdfs__label as prop1, n2.rdfs__label as prop2")
	    

	    prop1=[]
	    prop2=[]
	    
	    for record in result:
	        prop1.append(record["prop1"])
	        prop2.append(record["prop2"])



	    sub=[]
	    pred=[]
	    obj=[]
	    for i in range(len(prop1)):
	        data=db.run("MATCH (n1)-[r1:ns1__"+prop1[i]+"]->(n2) merge(n1)<-[r2:ns1__"+prop2[i]+"]-(n2) return n2.uri as subject,n1.uri as object")
	        
	        for record in data:
	            sub.append(record["subject"])
	            pred.append(prop2)
	            obj.append(record["object"])
	    
	    data={}
	    js=[]
	    dictn={}
	    data["subject"]=sub
	    data["predicate"]=pred
	    data["object"]=obj
	    js.append(data)
	    dictn["res"]=js
	    #print(json.dumps(dictn))

	    db.close()
	    return dictn
	    # print(sub)
	    
	    
	if(prop=="Functional"):
	    functional_prop=[]
	    property_uri=[]
	    i=0
	    uri=db.run(uri)
	    for record in uri:
	        uri=record["uri"]
	        print(uri)
	    result=db.run("match(n:owl__FunctionalProperty) return n.rdfs__label as prop ")
	    for record1 in result:
	        functional_prop.insert(i,record1["prop"])
	        i=i+1
	    print(functional_prop)
	    
	    nodes=[]
	    for properties in functional_prop:
	        data=db.run("match (n1)-[:ns1__"+properties+"]->(n2) with n1, count(*) as x where x > 1 return n1.uri as uri ")
	        for record in data:
	            nodes.append(record["uri"])

	    data={}
	    js=[]
	    dictn={}
	    data["nodes"]=nodes
	    js.append(data)
	    dictn["res"]=js
	    db.close()
	    print(dictn)
	    return dictn
  


  
# Main("Transitivity")