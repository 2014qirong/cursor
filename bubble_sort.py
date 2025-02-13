def bubble_sort(arr):
    """
    冒泡排序函数
    参数:
        arr: 需要排序的列表
    返回:
        排序后的列表
    """
    n = len(arr)
    # 遍历所有数组元素
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # 从头到尾遍历数组
            # 如果找到更大的元素，则交换
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def main():
    # 测试用例
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("原始数组:", test_array)
    
    sorted_array = bubble_sort(test_array.copy())
    print("排序后数组:", sorted_array)

    # 测试空数组
    empty_array = []
    print("\n空数组测试:")
    print("排序后:", bubble_sort(empty_array))

    # 测试已排序数组
    # 创建一个已经排序的测试数组
    sorted_test = [1, 2, 3, 4, 5]
    # 打印测试标题
    print("\n已排序数组测试:")
    # 对已排序数组进行排序并打印结果
    print("排序后:", bubble_sort(sorted_test))

    # 测试重复元素
    duplicate_array = [4, 2, 4, 1, 2, 1]
    print("\n重复元素数组测试:")
    print("原始数组:", duplicate_array)
    print("排序后:", bubble_sort(duplicate_array.copy()))


if __name__ == "__main__":
    main() 