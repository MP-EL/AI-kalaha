playingdict = {
                "Depth 4":      [4, False],
                "Depth 4 AB":   [4, True],
                "Depth 5":      [5, False],
                "Depth 5 AB":   [5, True]
                # "Depth 6":      [6, False],
                # "Depth 6 AB":   [6, True],
                # "Depth 7":      [7, False],
                # "Depth 7 AB":   [7, True],  
                # "Depth 8 AB":   [8, True]            
}

score = {}

for Key,[Depth,AB] in playingdict.items():
    temp_array = []
    for i in range(10):
        temp_array.append(i)
    
    temp_dict = {f'{Key}':temp_array}
    print(type(temp_array))
    score.update(temp_dict)
