from math import ceil, log
from mpyc.runtime import mpc


@mpc.coroutine
async def binary_search(sorted_list, element, secint):
    """
        Computes secret binary search on a secret list (seclist) sorted_list without letting
        any party obtain any information about the content of the list or the result.
        The result respectevely is a secret int containing either the index in which the searched element is located.
        Or a secint containing -1 if the element could not be found.
        If the searched value is present multiple times in the list, which element index will be printed is undefined.
        As of binary search sorted_list is required to be a sorted seclist containing elements of type secint.
        Furthermore element is also required to be of type secint.
    """
    lower = secint(0)
    upper = secint(len(sorted_list) - 1)
    steps = ceil(log(len(sorted_list), 2))
    for _ in range(steps):
        mid = (lower + upper) // secint(2)
        lower = mpc.if_else(sorted_list[mid] < element, mid + secint(1), lower)
        upper = mpc.if_else(sorted_list[mid] > element, mid - secint(1), upper)
        lower = mpc.if_else(sorted_list[mid] == element, mid, lower)
        upper = mpc.if_else(sorted_list[mid] == element, mid, upper)

    return mpc.if_else(sorted_list[lower] == element, lower, secint(-1))


@mpc.coroutine
async def binary_search_unsec(sortedList, element, secint):
    """
        Computes secret binary search on a normal list sorted_list containing secints.
        This function exposes some information about the list, since the indices on which the list is accessed are not secret and thus one could obtain which elements are smaller and larger to the searched element.
        Because required secrecy is missing anyways, the result respectevely is a normal int containing either the index in which the searched element is located.
        Or a -1 if the element could not be found.
        If the searched value is present multiple times in the list, which element index will be printed is undefined.
        As of binary search sorted_list is required to be a sorted seclist containing elements of type secint.
        Furthermore element is also required to be of type secint.
    """
    lower = 0
    upper = len(sortedList) - 1
    steps = ceil(log(len(sortedList), 2))
    for _ in range(steps):
        mid = (lower + upper) // 2
        lower = mpc.if_else(sortedList[mid] < element, mid + 1, lower)
        upper = mpc.if_else(sortedList[mid] > element, mid - 1, upper)
        lower = mpc.if_else(sortedList[mid] == element, mid, lower)
        upper = mpc.if_else(sortedList[mid] == element, mid, upper)

    return mpc.if_else(sortedList[lower] == element, lower, -1)


async def main():
    """
        A main method mainly used for testing the implemented binary search method.
        It lets each party input a value to a secret shared list, checks secretly whether given list contains a 5, then prints the contents of the list and the index of the first found five in that list.
    """
    await mpc.start()

    secint = mpc.SecInt()
    searchElement = secint(5)
    el = int(input("SAY NUMBER!!!:::"))
    randList = mpc.input(secint(el))
    seclist = mpc.seclist(randList)
    seclist.sort()
    index = binary_search_unsec(seclist, searchElement, secint)
    print(await mpc.output(list(seclist)))
    print(await mpc.output(index))

    await mpc.shutdown()

if __name__ == '__main__':
    mpc.run(main())
