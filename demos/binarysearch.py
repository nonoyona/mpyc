from math import ceil, log
from mpyc.runtime import mpc


@mpc.coroutine
async def binary_search(sortedList, element, secint):
    lower = secint(0)
    upper = secint(len(sortedList) - 1)
    steps = ceil(log(len(sortedList), 2))
    for _ in range(steps):
        mid = (lower + upper) // secint(2)
        lower = mpc.if_else(sortedList[mid] < element, mid + secint(1), lower)
        upper = mpc.if_else(sortedList[mid] > element, mid - secint(1), upper)
        lower = mpc.if_else(sortedList[mid] == element, mid, lower)
        upper = mpc.if_else(sortedList[mid] == element, mid, upper)

    return mpc.if_else(sortedList[lower] == element, lower, secint(-1))


@mpc.coroutine
async def binary_search_unsec(sortedList, element, secint):
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
