def insertion_sort(nums):
    comps = 0
    moves = 0
    n = len(nums)

    for i in range(1, n):
        cur = nums[i]
        k = i - 1
        while k >= 0:
            comps += 1
            if nums[k] <= cur:
                break
            nums[k + 1] = nums[k]
            moves += 1
            k -= 1
        nums[k + 1] = cur

    return nums, comps, moves


if __name__ == "__main__":
    data = [29, 3, 72, 15, 8, 41]
    print("before:", data)
    result, c, m = insertion_sort(data[:])
    print("after: ", result)
    print("comparisons =", c, "| shifts =", m)
