"""A simple interactive CYK parser, for educational purposes"""

import re

def main():
	terminals=get_terminals()
	nonterminals=get_nonterminals()
	rules=get_rules(terminals,nonterminals)
	start=get_start(nonterminals)
	print('Enter a string in order to check whether in is in the language. Enter an empty string to exit.')
	while True:
		print('Enter a string: ',end='')
		string=input().strip()
		if len(string)==0:
			return
		for c in string:
			if not c in terminals:
				print("Illegal string - character %s isn't a terminal."%c)
				valid=False
				break
		if(cyk(terminals,nonterminals,rules,start,string)):
			print('"%s" is a member of the language.'%string)
		else:
			print('"%s" is not a member of the language.'%string)

def get_terminals():
	terminals=set()
	print('Enter the terminals, or an empty string when done:')
	while True:
		print('Enter a terminal: ',end='')
		terminal=input().strip()
		if len(terminal)==0:
			if len(terminals)==0:
				print("You must enter at least one terminal.")
				continue
			return terminals
		terminals.add(terminal)
		
def get_nonterminals():
	nonterminals=set()
	print('Enter the nonterminals, or an empty string when done:')
	while True:
		print('Enter a nonterminal: ',end='')
		nonterminal=input().strip()
		if len(nonterminal)==0:
			if len(nonterminals)==0:
				print("You must enter at least one nonterminal.")
				continue
			return nonterminals
		nonterminals.add(nonterminal)
		
def get_rules(terminals,nonterminals):
	rules=[]
	print("A chomsky normal rule is of type 'A->a' or 'A->B C', where 'a' is a terminal and 'A','B' and 'C' are nonterminals.")
	print('Enter the rules, or an empty string when done:\n')
	while True:
		print("Enter a rule of type 'A->a' or 'A->B C': ",end='')
		match=None
		type=None
		while True:
			rule=input().strip()
			if len(rule)==0:
				if len(rules)==0:
					print("You must enter at least one rule.")
					continue
				return rules
			match=re.match(r'([^ \t\-\>]+)\-\>([^ \t\-\>]+)(?: ([^ \t\-\>]+))?',rule)
			if not match is None:
				break
			print("Could not parse rule. Please enter a rule of type 'A->a' or 'A->B C':")
		groups=match.groups()
		source=groups[0]
		if not source in nonterminals:
			print("Invalid rule: source '%s' is not a nonterminal"%source)
			continue
		if groups[2] is None:
			target=groups[1]
			if not target in terminals:
				print("Invalid rule: target '%s' is not a terminal"%target)
				continue
			rules.append((source,[target]))
		else:
			targets=groups[1:]
			for target in targets:
				if not target in nonterminals:
					print("Invalid rule: target '%s' is not a nonterminal"%target)
					continue
			rules.append((source,targets))
		
def get_start(nonterminals):
	while True:
		print("Enter a starting nonterminal:",end='')
		start=input().strip()
		if start in nonterminals:
			return start
		print("Starting symbol must be a nonterminal.")
			
def cyk(terminals,nonterminals,rules,start,string):
	p=dict()
	n=len(string)
	for i in range(1,n+1):
		for j in range(1,n+1):
			for k in nonterminals:
				p[(i,j,k)]=False
	for i in range(1,n+1):
		for rule in rules:
			if len(rule[1])==1:
				if rule[1][0]==string[i-1]:
					p[(i,1,rule[0])]=True
	for i in range(2,n+1):
		for j in range(1,n-i+2):
			for k in range(1,i):
				for rule in rules:
					if len(rule[1])==2:
						if p[(j,k,rule[1][0])] and p[(j+k,i-k,rule[1][1])]:
							p[(j,i,rule[0])]=True
	return p[(1,n,start)]

if(__name__=='__main__'):
	main()