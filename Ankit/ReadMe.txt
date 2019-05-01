backend.py
*************************
Has code for static rules like transitiviy, Inverse, Functional Properties


ruleEngine.py
*************************
Requirements
1.Neo4j server must be installed and running.
2.Graph must be created and running
3. For Django server must be up and running
4. Some commands and queries are written in file Movie_Actors.doc for reference


*************************


Code for user defined rules
*************************
Format:
IF
	SUB=______________  PRED=________________  OBJECT=_________________   (AND/OR)  [ADD RULE]
	SUB=______________  PRED=________________  OBJECT=_________________   (AND/OR)  [ADD RULE]
THEN

	SUB=______________  PRED=________________  OBJECT=_________________   
**************************
ASSUMPTIONS:
1.Atmost one variable has to be there in any IF condition (?variable)
2.Then condition can have exactly one variable
3.If say one variable of movie (?movie) is used then the same variable must be used anywhere else where ?movie has to be specifed
4.User may enter any new predicates in the "then statement" but these predicated will only be visible in the result of the query and NOT in the ontology.
	means the structural node for the new predicate will not be made, only instances will be created.
5.The List for predefined SUB, PREDS, OBJS will be there in the a.html page. Exact same spelling of the words must be used
6.There can be any number of the "IF" conditions

7.UI ERROR: whenever ADD RULE is clicked the previous selection for the predicates in the list is refreshed.
