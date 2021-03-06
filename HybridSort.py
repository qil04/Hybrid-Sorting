"""
Name: Chris Li
Project 2 - Hybrid Sorting
CSE 331 Fall 2020
Professor Sebnem Onsay
"""
from typing import List, Any, Dict


def hybrid_sort(data: List[Any], threshold: int) -> None:
    """
    Wrapper function to use merge_sort() as a Hybrid Sorting Algorithm.
    :param data: [List] of str or int to be sorted.
                 [int] int representing the size of the data at which insertion sort should be used.
    :return: None
    Time Complexity: average case: O(n*log(n))
                     worst case: O(n^2)
    Space Complexity: O(n)
    """
    merge_sort(data, threshold)

def inversions_count(data: List[Any]) -> int:
    """
    Wrapper function to use merge_sort() to retrieve the inversion count.
    :param data: [List] of str or int to be sorted.
    :return: [int] representing inversion count.
    Time Complexity: O(n*log(n))
    Space Complexity: O(n)
    """
    return merge_sort(data)

def merge_sort(data: List[Any], threshold: int = 0) -> int:
    """
    Perform a merge sort to sort the list and calculate the inversion count.
    :param data: [List] of str or int to be sorted.
    :return: [int] representing inversion count. 0 if threshold > 0.
    Time Complexity: average case: O(n*log(n))
                     worst case: O(n^2)
    Space Complexity: O(n)
    """
    n_lst = len(data)
    if n_lst < 2:
        return 0 #sorted in order
    mid = n_lst//2
    left, right = data[0:mid], data[mid:n_lst]
    int_left, int_right = merge_sort(left), merge_sort(right)
    if len(left) < threshold or len(right) < threshold:
        insertion_sort(data)
        return 0
    else:
        return merge(left, right, data) + int_left + int_right

def merge(left: List[Any], right: List[Any], data: List[Any]):
    """
    Merge partitioned list and calculate inner inversions in an order manner.
    :param data: [List] of left partitioned to be sorted.
                 [List] of right partitioned to be sorted.
                 [List] origin data list
    :return: [int] representing inner inversion count.
    """
    i = j = 0
    count = 0
    while (i + j) < len(data):
        if  i < len(left) and j < len(right):
            if left[i] < right[j]:
                data[i+j] = left[i]
                i = i + 1
            else:
                data[i+j] = right[j]
                j = j + 1
        elif i == len(left):
            data[i+j] = right[j]
            j += 1
        elif j == len(right):
            data[i+j] = left[i]
            i += 1
    for item_l in left:
        for item_j in right:
            if item_l > item_j:
                count += 1
    return count

def insertion_sort(data: List[Any]) -> None:
    """
    Given a list of values, perform an insertion sort to sort the list.
    :param data: [List] of str or int to be sorted.
    :return: None
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    for index in range(len(data)):
        pos = index
        while pos > 0 and data[pos] < data[pos - 1]:
            temp = data[pos]
            data[pos] = data[pos-1]
            data[pos-1] = temp
            pos -= 1

def find_match(user_interests: List[str], candidate_interests: Dict[str, List]) -> str:
    """
    Given a list of user interests, ranked in order of preference,
    and a mapping of candidates to their interest rankings, return the name
    of the candidate whose interest ranking most closely match the user's.
    :param data: [list] user_interests where interests in order of preference ranking.
                 [dict] candidate_interests where keys are candidate names (str), and
                        values are corresponding interest rankings (List(str)).
    :return: Name of candidate match
    Time Complexity: O(k*n*log(n))
    Space Complexity: O(k*n)
    """
    for item in user_interests:
        rank = user_interests.index(item) + 1
        for value in candidate_interests.values():
            if item in value:
                if value.count(item) != 1:
                    value_c = value
                    pos = value_c.index(item)
                    value[pos] = rank
                pos_chk = value.index(item)
                value[pos_chk] = rank
    pre_inv_c = 10000 #enough big to set pre_inv_c in the loop
    target_name = ''
    for k, item in candidate_interests.items():
        inv_c = inversions_count(item)
        if inv_c < pre_inv_c:
            target_name = k
            pre_inv_c = inv_c
    return target_name
