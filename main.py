import random


def loadMatrix(sciezka):
    file = open(sciezka, 'r')
    file_reading = []
    matrix = []
    for line in file:
        file_reading.append(line.split())
    for i in file_reading[1:]:
        matrix.append(i)
    x = 1
    for i in range(len(matrix) - 1):
        for j in range(x, len(matrix)):
            matrix[i].append(matrix[j][i])
        x = x + 1
    print('distance matrix:')
    for row in matrix:
        print(row)
    return matrix


def createIndividuals(matrix, paths_amount):
    pathsRandom = []
    pathsTemp = []
    for i in range(paths_amount):
        pathsTemp.append(random.sample(range(len(matrix)), len(matrix)))
        if pathsTemp[i] not in pathsRandom:
            pathsRandom.append(pathsTemp[i])
    return pathsRandom


def rate(matrix, pathsRandom):
    lengthsOfRoutes = []
    routeLength = 0
    for i in range(len(pathsRandom)):
        pathsRandom[i].append(pathsRandom[i][0])  # dodanie do konca listy punktu startowego
        for j in range(len(pathsRandom[i]) - 1):
            routeLength += int(matrix[pathsRandom[i][j]][pathsRandom[i][j + 1]])
        lengthsOfRoutes.append(routeLength)
        routeLength = 0
        del pathsRandom[i][
            -1]  # usuwa z końca listy punkt startowy (ocene liczy wcześniej z wracaniem do punktu startowego)
    return [lengthsOfRoutes, pathsRandom]


def turnamentSelection(trasyRnd, k, n):
    winners = []
    drawn = []
    for j in range(n):
        index = random.sample(range(0, len(trasyRnd)), k)
        for i in range(len(index)):
            drawn.append(trasyRnd[index[i]])
        best = rate(matrix, drawn)
        winners.append(drawn[best[0].index(min(best[0]))])
        drawn.clear()
    return winners


def crossing(routes, crossing_parameter):
    tempRoutes = []
    crossedRoutes = []
    for i in range(len(routes)):
        isLast = False
        if (i == len(routes) - 1):
            isLast = True
        if (isLast == True):
            check = 0
        else:
            check = i + 1
        middles = []
        tempRoutes.append(routes[i].copy())
        sep = (random.sample(range(0, len(routes[i]) + 1), 2))
        sep.sort()
        middles.append(routes[i][sep[0]:sep[1]])
        middles.append(routes[check][sep[0]:sep[1]])
        for j in range(len(tempRoutes[i])):
            tempRoutes[i][j] = 'X'
        for j in range(len(middles[0])):  # WYPEŁNIJ ŚRODKIEM KTÓRY SIĘ NIE ZMIENIA
            tempRoutes[i][(sep[0] + j)] = middles[0][j]

        def cross(length, indexInput=None):
            if indexInput is None:
                indexInput = length
            if routes[check][length] in tempRoutes[i]:
                index = (tempRoutes[i].index(routes[check][length]))
                return cross(index, indexInput)
            else:
                tempRoutes[i][indexInput] = routes[check][length]
                return 0

        rnd = random.uniform(0, 1)
        if rnd < crossing_parameter:
            for length in range(len(tempRoutes[i])):
                if (tempRoutes[i][length]) == 'X':
                    cross(length)
            crossedRoutes.append(tempRoutes[i])
        else:
            crossedRoutes.append(routes[i])
    return crossedRoutes


def mutation(routes, mutation_parameter):
    middles = []
    tempRoutes = []
    routerMutated = []
    for i in range(len(routes)):
        sep = (random.sample(range(0, len(routes[i]) + 1), 2))
        sep.sort()
        middles.append(routes[i][sep[0]:sep[1]])
        middles[i].reverse()
        tempRoutes.append(routes[i])
        for j in range(len(middles[i])):
            tempRoutes[i][(sep[0] + j)] = middles[i][j]
        rnd = random.uniform(0, 1)
        if rnd < mutation_parameter:
            routerMutated.append(tempRoutes[i])
        else:
            routerMutated.append(routes[i])
    return routerMutated


def algorithm(matrix, number_of_executions):
    result = individuals
    for i in range(number_of_executions):
        winners = turnamentSelection(result, k, n)
        crossed_routes = crossing(winners, par_k)
        result = mutation(crossed_routes, par_m)
        rates = rate(matrix, result)
    min_index = rates[0].index(min(rates[0]))
    print(*rates[1][min_index], sep='-', end=' ')
    print(min(rates[0]))


routesNumber = 100  # ile tras (do stworzenia różnych osobników) wylosować
k = 50  # ilu osobnikow losujemy do selekcji turniejowej, wiecej = wiekszy nacisk selektywny
n = 100  # ile razy losujemy osobnikow i wybieramy najlepszego z nich
par_k = 0.75
par_m = 0.2
iterations = 500
# złote proporcje dla berlina - ileTras=100, k=50, n=100, par_k=0.5, par_m=0.5 algorytm 1000 razy

# dla par_k - 0.8 i par_m - 0.3 minimum na berlinie 7667
matrix = loadMatrix('berlin52.txt')
print("TRWA LICZENIE...")
individuals = createIndividuals(matrix, routesNumber)
algorithm(matrix, iterations)
