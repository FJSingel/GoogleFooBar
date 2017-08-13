def answer(l):
    # This seems rather expensive
    results = 0
    
    def too_slow(l):
        results = 0
        while len(l) > 2:
            x = l.pop(0)
            # print x
            for index in range(len(l))[:-1]:
                y = l[index]
                # print str(x) + ',' + str(y)
                if (y%x==0):
                    #Look for 3rd
                    for z in l[index+1:]:
                        # print str(x) + ',' + str(y) + ',' + str(z)
                        if (z%y==0):
                            # print "DING"
                            results += 1    
                            # results.append([x,y,z])
        return results
        
    def filtering(l):
        #Maybe I can do with filtering...
        results = 0
        while len(l) > 2:
            i = l.pop(0)
            filtered1 = [j for j in l if j%i == 0]
            filtered2 = [k for k in filtered1 if k%j == 0]
            print filtered1
            print filtered2
        #Eh, I think I can do if I figure out how to encode the values right
        return results
    
    def refactored(l):
        num_divs_after = [0] * len(l)
        total = 0
        #Skip checking last index
        for index in xrange(len(l)-2, -1, -1):
            for search_index in xrange(index+1, len(l)):
                if l[search_index]%l[index] == 0:
                    num_divs_after[index] += 1
                    total += num_divs_after[search_index]
        return total
    
return refactored(l)