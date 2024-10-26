# Name: John Fletcher
# OSU Email: fletjohn@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2
# Due Date: 10/30/2024
# Description: Implementation of the dynamic array data
#              structure and associated methods

from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        INPUTS: new_capacity [int]
        RETURNS: NONE
        DESCRIPTION: Function resizes array to the size of new_capacity
        """

        #check if new_capacity input is negative
        if new_capacity <= 0:
            return
        elif new_capacity < self._size:
            return
        else:
            dummy_array = StaticArray(new_capacity)

            for data_index in range(self.length()):
                dummy_array[data_index] = self._data[data_index]

            self._capacity = new_capacity
            self._data = dummy_array


    def append(self, value: object) -> None:
        """
            INPUTS: value [object]
            RETURNS: NONE
            DESCRIPTION: appends a given value to the data array and resizes
                         the array to fit the new value
        """
        if self._size >= self._capacity:
            self.resize(self._capacity * 2)

        self._size += 1
        self._data[self._size - 1] = value

    def insert_at_index(self, index: int, value: object) -> None:
        """
            INPUTS: index [int]
                    value [object]
            RETURNS:NONE
            DESCRIPTION:inserts value at desired index and shifts all values above
                        the index to the right one space to make room for the input
                        value

        """
        if index < 0 or index > self._size:
            raise DynamicArrayException


        #resizes to 2x the original size if array is already full
        if self._size == self._capacity:
            self.resize(self._capacity * 2)

        self._size += 1

        #in-place shift right operation to update array and make space at desired
        #index for the new value
        for indices in range(self._size - index - 1):
            index_shift = self._size - indices - 1
            previous_value = self.get_at_index(index_shift - 1)
            self.set_at_index(index_shift, previous_value)

        #Sets value at desired index
        self.set_at_index(index, value)


    def remove_at_index(self, index: int) -> None:
        """
            INPUTS: index [int]
            RETURNS: NONE
            DESCRIPTION: This function removes a value from an array and
                         then shifts the contents of the array left for all
                         values of index more than that of the index of the
                         value that is being removed

        """
        #raises exception if index value is out of bounds
        if index < 0 or index > self._size - 1:
            raise DynamicArrayException

        if self._size < 0.25 * self._capacity and self._capacity > 10:
            #prevents array from being reduced to a size smaller than 10
            if 10 <= int(self._capacity / 2):
                self.resize(int(self._size * 2))
            else:
                self.resize(10)

        #very similar to the in place shift right but now
        #shifting values to the left instead
        for indices in range(self._size - index - 1):
            index_shift = indices + index
            next_value = self.get_at_index(index_shift + 1)
            self.set_at_index(index_shift, next_value)

        #reduces array size by 1 since we have removed one element
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Slices the current array starting from start_index and extending by size elements.
        Returns a new DynamicArray containing the sliced elements.
        """
        # Create a new DynamicArray for the slice
        sliced_array = DynamicArray()

        # Raises an exception if start_index or size are out of range
        if size < 0 or start_index < 0 or start_index > self._size - 1 or start_index + size > self._size:
            raise DynamicArrayException

        # Append each element in the specified slice range to the new array
        for i in range(size):
            sliced_array.append(self._data[i + start_index])

        return sliced_array

    def map(self, map_func) -> "DynamicArray":
        """
            INPUTS:hh
            RETURNS:
            DESCRIPTION:

        """

        output_array = DynamicArray()
        output_array.resize(self._capacity)
        for i in range(self._size):
            output_array.insert_at_index(i, map_func(self._data[i]))

        return output_array

    def filter(self, filter_func) -> "DynamicArray":
        """
        Filters the DynamicArray based on the provided filter function and returns a new DynamicArray
        containing only the elements that meet the filter criteria.
        """
        output_array = DynamicArray()

        for i in range(self._size):
            if filter_func(self._data[i]):
                output_array.append(self._data[i])

        # Resize the output array to the actual number of elements added
        if output_array.length() > 0:
            output_array.resize(output_array.length())  # Resize to the actual size
        else:
            output_array.resize(4)  # Ensure minimum capacity if no elements

        return output_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
            INPUTS:
            RETURNS:
            DESCRIPTION:

        """
        # Check if the array is empty
        if self._size == 0:
            return initializer  # Return the initializer, or None if not provided

        # Set initial value based on whether initializer is provided
        value = initializer if initializer is not None else self._data[0]

        # Start index depending on whether initializer is provided
        start_index = 1 if initializer is None else 0

        # Perform the reduction
        for i in range(start_index, self._size):
            element = self._data[i]
            value = reduce_func(value, element)

        return value


def chunk(arr: DynamicArray) -> "DynamicArray":
    """
    Splits the input DynamicArray into chunks of non-descending sequences and returns a new DynamicArray.
    """
    result = DynamicArray()
    chunk_array = DynamicArray()

    if arr.length() > 0:
        # Start the first chunk with the first element
        chunk_array.append(arr[0])

        for i in range(1, arr.length()):
            # If non-descending, add to the current chunk
            if arr[i] >= arr[i - 1]:
                chunk_array.append(arr[i])
            else:
                # Append the completed chunk to result
                result.append(chunk_array)
                # Start a new chunk with the current element (without using a list)
                chunk_array = DynamicArray()
                chunk_array.append(arr[i])

        # Append the last chunk if it exists
        if chunk_array.length() > 0:
            result.append(chunk_array)

    return result



def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds the mode(s) of the sorted array `arr` and returns a tuple containing
    a DynamicArray of the mode(s) and their frequency count.
    """
    mode_array = DynamicArray()  # Start with an empty DynamicArray for the modes
    current_element = arr[0]
    current_count = 1
    max_count = 1

    # Initialize mode array with the first element if max_count == 1
    mode_array.append(current_element)

    for i in range(1, arr.length()):
        if arr[i] == current_element:
            current_count += 1  # Increment count for the current element
        else:
            # If current count exceeds max, reset mode_array and update max_count
            if current_count > max_count:
                max_count = current_count
                mode_array = DynamicArray()  # Reset mode_array
                mode_array.append(current_element)  # Add the new mode
            elif current_count == max_count and current_element != mode_array[0]:
                mode_array.append(current_element)  # Add to mode_array if frequency matches max

            # Update to the new element
            current_element = arr[i]
            current_count = 1

    # Final check for the last element
    if current_count > max_count:
        mode_array = DynamicArray([current_element])  # Set the last element as mode
        max_count = current_count
    elif current_count == max_count:
        mode_array.append(current_element)  # Add the last element if it matches max frequency

    return mode_array, max_count

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    def print_chunked_da(arr: DynamicArray):
        if len(str(arr)) <= 100:
            print(arr)
        else:
            print(f"DYN_ARR Size/Cap: {arr.length()}/{arr.get_capacity()}")
            print('[\n' + ',\n'.join(f'\t{chunk}' for chunk in arr) + '\n]')

    print("\n# chunk example 1")
    test_cases = [
        [10, 20, 30, 30, 5, 10, 1, 2, 3, 4],
        ['App', 'Async', 'Cloud', 'Data', 'Deploy',
         'C', 'Java', 'Python', 'Git', 'GitHub',
         'Class', 'Method', 'Heap']
    ]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# chunk example 2")
    test_cases = [[], [261], [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# find_mode example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
