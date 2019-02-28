import numpy as np
import tensorflow as tf


def cardinality_intersection_of_tags(set1, set2):
    return len(set1.intersection(set2))

def cardinality_s1_minus_s2(set1, set2):
    return len(set1.difference(set2))

def cardinality_s2_minus_s1(set1, set2):
    return len(set2.difference(set1))
    