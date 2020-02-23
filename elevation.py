"""Assignment 2 functions."""

from typing import List

THREE_BY_THREE = [[1, 2, 1],
                  [4, 6, 5],
                  [7, 8, 9]]

FOUR_BY_FOUR = [[1, 2, 6, 5],
                [4, 5, 3, 2],
                [7, 9, 8, 1],
                [1, 2, 1, 4]]

UNIQUE_3X3 = [[1, 2, 3],
              [9, 8, 7],
              [4, 5, 6]]

UNIQUE_4X4 = [[10, 2, 3, 30],
              [9, 8, 7, 11],
              [4, 5, 6, 12],
              [13, 14, 15, 16]]


def compare_elevations_within_row(elevation_map: List[List[int]], map_row: int,
                                  level: int) -> List[int]:
    """Return a new list containing the three counts: the number of
    elevations from row number map_row of elevation map elevation_map
    that are less than, equal to, and greater than elevation level.

    Precondition: elevation_map is a valid elevation map.
                  0 <= map_row < len(elevation_map).

    >>> compare_elevations_within_row(THREE_BY_THREE, 1, 5)
    [1, 1, 1]
    >>> compare_elevations_within_row(FOUR_BY_FOUR, 1, 2)
    [0, 1, 3]

    """
    
    less = 0
    equal = 0
    greater = 0
    lst = []
    for elevation in elevation_map[map_row]:
        if elevation < level:
            less += 1
        elif elevation == level:
            equal += 1
        else:
            greater += 1
    
    lst.extend([less, equal, greater])
    return lst    


def update_elevation(elevation_map: List[List[int]], start: List[int],
                     stop: List[int], delta: int) -> None:
    """Modify elevation map elevation_map so that the elevation of each
    cell between cells start and stop, inclusive, changes by amount
    delta.

    Precondition: elevation_map is a valid elevation map.
                  start and stop are valid cells in elevation_map.
                  start and stop are in the same row or column or both.
                  If start and stop are in the same row,
                      start's column <=  stop's column.
                  If start and stop are in the same column,
                      start's row <=  stop's row.
                  elevation_map[i, j] + delta >= 1
                      for each cell [i, j] that will change.

    >>> THREE_BY_THREE_COPY = [[1, 2, 1],
    ...                        [4, 6, 5],
    ...                        [7, 8, 9]]
    >>> update_elevation(THREE_BY_THREE_COPY, [1, 0], [1, 1], -2)
    >>> THREE_BY_THREE_COPY
    [[1, 2, 1], [2, 4, 5], [7, 8, 9]]
    >>> FOUR_BY_FOUR_COPY = [[1, 2, 6, 5],
    ...                      [4, 5, 3, 2],
    ...                      [7, 9, 8, 1],
    ...                      [1, 2, 1, 4]]
    >>> update_elevation(FOUR_BY_FOUR_COPY, [1, 2], [3, 2], 1)
    >>> FOUR_BY_FOUR_COPY
    [[1, 2, 6, 5], [4, 5, 4, 2], [7, 9, 9, 1], [1, 2, 2, 4]]

    """
    if start == stop:
        elevation_map[start[0]][start[1]] += delta
    elif start[0] == stop[0]:
        for i in range(start[1], stop[1] + 1):
            elevation_map[start[0]][i] += delta
    elif start[1] == stop[1]:
        for i in range(start[0], stop[0] + 1):
            elevation_map[i][start[1]] += delta        


def get_average_elevation(elevation_map: List[List[int]]) -> float:
    """Return the average elevation across all cells in the elevation map
    elevation_map.

    Precondition: elevation_map is a valid elevation map.

    >>> get_average_elevation(UNIQUE_3X3)
    5.0
    >>> get_average_elevation(FOUR_BY_FOUR)
    3.8125
    """
    
    total = 0
    for row in elevation_map:
        for column in row:
            total = total + column
    return total / len(elevation_map)**2


def find_peak(elevation_map: List[List[int]]) -> List[int]:
    """Return the cell that is the highest point in the elevation map
    elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  Every elevation value in elevation_map is unique.

    >>> find_peak(UNIQUE_3X3)
    [1, 0]
    >>> find_peak(UNIQUE_4X4)
    [0, 3]
    """
    
    highest_point = []
    max_height = 0
    for r in range(len(elevation_map)):
        for c in range(len(elevation_map[0])):
            if elevation_map[r][c] > max_height:
                max_height = elevation_map[r][c]
                highest_point.clear()
                highest_point.extend([r, c])
    return highest_point


def is_sink(elevation_map: List[List[int]], cell: List[int]) -> bool:
    """Return True if and only if cell exists in the elevation map
    elevation_map and cell is a sink.

    Precondition: elevation_map is a valid elevation map.
                  cell is a 2-element list.

    >>> is_sink(THREE_BY_THREE, [0, 5])
    False
    >>> is_sink(THREE_BY_THREE, [0, 2])
    True
    >>> is_sink(THREE_BY_THREE, [1, 1])
    False
    >>> is_sink(FOUR_BY_FOUR, [2, 3])
    True
    >>> is_sink(FOUR_BY_FOUR, [3, 2])
    True
    >>> is_sink(FOUR_BY_FOUR, [1, 3])
    False
    """
    
    max_r = len(elevation_map) - 1
    max_c = len(elevation_map[0]) -1     
    if cell[0] > max_r or cell[0] < 0 or cell[1] > max_c or cell[1] < 0:
        return False
    sink = sink_elevation(elevation_map, cell)              
    return sink == elevation_map[cell[0]][cell[1]]


def find_local_sink(elevation_map: List[List[int]],
                    cell: List[int]) -> List[int]:
    """Return the local sink of cell cell in elevation map elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  elevation_map contains no duplicate elevation values.
                  cell is a valid cell in elevation_map.

    >>> find_local_sink(UNIQUE_3X3, [1, 1])
    [0, 0]
    >>> find_local_sink(UNIQUE_3X3, [2, 0])
    [2, 0]
    >>> find_local_sink(UNIQUE_4X4, [1, 3])
    [0, 2]
    >>> find_local_sink(UNIQUE_4X4, [2, 2])
    [2, 1]
    """
    
    k = cell[0]
    l = cell[1]
    
    lowest = sink_elevation(elevation_map, cell)
    
    for r in range(len(elevation_map)):
        if lowest in elevation_map[r]:
            k = r
            l = elevation_map[r].index(lowest)
    return [k, l]


def can_hike_to(elevation_map: List[List[int]], start: List[int],
                dest: List[int], supplies: int) -> bool:
    """Return True if and only if a hiker can go from start to dest in
    elevation_map without running out of supplies.

    Precondition: elevation_map is a valid elevation map.
                  start and dest are valid cells in elevation_map.
                  dest is North-West of start.
                  supplies >= 0

    >>> map = [[1, 6, 5, 6],
    ...        [2, 5, 6, 8],
    ...        [7, 2, 8, 1],
    ...        [4, 4, 7, 3]]
    >>> can_hike_to(map, [3, 3], [2, 2], 10)
    True
    >>> can_hike_to(map, [3, 3], [2, 2], 8)
    False
    >>> can_hike_to(map, [3, 3], [3, 0], 7)
    True
    >>> can_hike_to(map, [3, 3], [3, 0], 6)
    False
    >>> can_hike_to(map, [3, 3], [0, 0], 18)
    True
    >>> can_hike_to(map, [3, 3], [0, 0], 17)
    False

    """
    n_elevation_diff = w_elevation_diff = 0
    while start != dest and supplies >= 0:
        n_elevation_diff = abs(elevation_map[start[0]][start[1]] 
                               - elevation_map[start[0] - 1][start[1]])        
        w_elevation_diff = abs(elevation_map[start[0]][start[1]] 
                               - elevation_map[start[0]][start[1] - 1]) 
        if start[0] == dest[0]:           
            supplies = supplies - w_elevation_diff
            start[1] = start[1] - 1
        elif start[1] == dest[1]:
            supplies = supplies - n_elevation_diff
            start[0] = start[0] - 1                
        else:
            if n_elevation_diff <= w_elevation_diff:
                supplies = supplies - n_elevation_diff
                start[0] = start[0] - 1                            
            elif n_elevation_diff > w_elevation_diff:
                supplies = supplies - w_elevation_diff
                start[1] = start[1] - 1                                                                               
        if start == dest and supplies >= 0:
                return True
    return False


def get_lower_resolution(elevation_map: List[List[int]]) -> List[List[int]]:
    """Return a new elevation map, which is constructed from the values
    of elevation_map by decreasing the number of elevation points
    within it.

    Precondition: elevation_map is a valid elevation map.

    >>> get_lower_resolution(
    ...     [[1, 6, 5, 6],
    ...      [2, 5, 6, 8],
    ...      [7, 2, 8, 1],
    ...      [4, 4, 7, 3]])
    [[3, 6], [4, 4]]
    >>> get_lower_resolution(
    ...     [[7, 9, 1],
    ...      [4, 2, 1],
    ...      [3, 2, 3]])
    [[5, 1], [2, 3]]

    """
    if len(elevation_map) < 2:
        return elevation_map
    else:
        new_map = []
        if len(elevation_map) % 2 == 1:
            for i in range(0, len(elevation_map) - 1, 2):
                new_map.append([])
                for n in range(0, len(elevation_map) - 1, 2):               
                    new_map[-1].append((elevation_map[i][n] 
                                        + elevation_map[i][n + 1] 
                                        + elevation_map[i + 1][n] 
                                        + elevation_map[i + 1][n + 1]) // 4)           
                new_map[-1].append((elevation_map[i][-1] 
                                    + elevation_map[i + 1][-1]) // 2)   
            new_map.append([])
            for n in range(0, len(elevation_map) - 1, 2):
                new_map[-1].append((elevation_map[-1][n] 
                                    + elevation_map[-1][n + 1]) // 2)
            new_map[-1].append(elevation_map[-1][-1])                
        else:
            for i in range(0, len(elevation_map), 2):
                new_map.append([])
                for n in range(0, len(elevation_map), 2):
                    new_map[-1].append((elevation_map[i][n] 
                                        + elevation_map[i][n + 1] 
                                        + elevation_map[i + 1][n] 
                                        + elevation_map[i + 1][n + 1]) // 4)
            
    return new_map    
    
    
# helper function for is_sink and find_local_sink
def sink_elevation(elevation_map: List[List[int]], cell: List[int]) -> int:
    """ Return the elevation of local sink of cell in elevation_map.
    
    Precondition: elevation_map is a valid elevation map.
                  cell is a 2-element list and is a valid cell in elevation_map.
    
    >>> sink_elevation(UNIQUE_3X3, [2, 0])
    4
    >>> sink_elevation(THREE_BY_THREE, [1, 1])
    1
    
    """
    
    i = cell[0]
    j = cell[1]
    max_r = len(elevation_map) - 1
    max_c = len(elevation_map[0]) -1  
    lowest = elevation_map[i][j]
    lowest = min(elevation_map[max(0, i-1)][max(0, j-1)], lowest)
    lowest = min(elevation_map[max(0, i-1)][j], lowest)
    lowest = min(elevation_map[max(0, i-1)][min(j+1, max_c)], lowest)
    lowest = min(elevation_map[i][max(0, j-1)], lowest)
    lowest = min(elevation_map[i][min(j+1, max_c)], lowest)
    lowest = min(elevation_map[min(max_r, i+1)][max(0, j-1)], lowest)
    lowest = min(elevation_map[min(max_r, i+1)][j], lowest)
    lowest = min(elevation_map[min(max_r, i+1)][min(max_c, j+1)], lowest)
    
    return lowest
