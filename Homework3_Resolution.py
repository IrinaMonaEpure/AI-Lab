# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 11:58:04 2020

@author: irina
"""

# TODO
from LPTester import *
from Lab08 import *

from copy import deepcopy
from functools import reduce

# In this cell there are several functions used internally

dummy = make_atom("P")
[and_name, or_name, neg_name] = [get_head(s) for s in [make_and(dummy, dummy), make_or(dummy, dummy), make_neg(dummy)]]
def pFail(message, f):
    print(message + " <" + str(f) + ">")
    return False
def check_term(T):
    if is_constant(T):
        return (get_value(T) is not None) or pFail("The value of the constant is None", T)
    if is_variable(T):
        return (get_name(T) is not None) or pFail("The name of the variable is None", T)
    if is_function_call(T):
        return not [t for t in get_args(T) if not check_term(t)] and \
            (get_head(T) is not None or pFail("Function is not callable", T))
    return pFail("Term is not one of constant, variable or function call", T)
def check_atom(A):
    if is_atom(A):
        return not [t for t in get_args(A) if not check_term(t)] and \
            (get_head(A) is not None or pFail("Predicate name is None", A))
    return pFail("Is not an atom", A)
def check_sentence(S):
    if is_atom(S):
        return check_atom(S)
    if is_sentence(S):
        if get_head(S) in [and_name, or_name]:
            return (len(get_args(S)) >= 2 or pFail("Sentence has too few operands", S)) \
                and not [s for s in get_args(S) if not check_sentence(s)]
        if get_head(S) == neg_name:
            return (len(get_args(S)) == 1 or pFail("Negative sentence has not just 1 operand", S)) \
                and check_sentence(get_args(S)[0])
    return pFail("Not sentence or unknown type", S)

def add_statement(kb, conclusion, *hypotheses):
    s = conclusion if not hypotheses else make_or(*([make_neg(s) for s in hypotheses] + [conclusion]))
    if check_sentence(s):
        kb.append(s)
        print("OK: Added statement " + print_formula(s, True))
        return True
    print("-- FAILED CHECK: Sentence does not check out <"+print_formula(s, True)+"><" + str(s) + ">")
    return False

var_no = 0;

def assign_next_var_name():
    global var_no
    var_no += 1
    return "v" + str(var_no)

def gather_vars(S):
    return [get_name(S)] if is_variable(S) else \
        [] if not has_args(S) else reduce(lambda res, a: res + gather_vars(a), get_args(S), [])

def make_unique_var_names(KB):
    global var_no
    var_no = 0
    return [substitute(S, {var: make_var(assign_next_var_name()) for var in gather_vars(S)}) for S in KB]           
            
def print_KB(KB):
    print("KB now:")
    for s in KB:
        print("\t\t\t" + print_formula(s, True))
        
def is_positive_literal(L):
    return is_atom(L)

def is_negative_literal(L):
    global neg_name
    return get_head(L) == neg_name and is_positive_literal(get_args(L)[0])

def is_literal(L):
    return is_positive_literal(L) or is_negative_literal(L)

