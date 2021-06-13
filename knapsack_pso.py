#------------------------------------------------------------------------------
#
#   Yusuf DURSUN
#   Python üzerinde Parçacık Sürü Optimizasyonunun Kullanılarak Knapsack(Sırt Çantası) Probleminin Dinamik Bir Şekilde Çözülmesi
#
#------------------------------------------------------------------------------

# Include project dependencies...
import matplotlib.pyplot as plt
import random
import math


# Defining global variables [Important: Other variables and running the algorithm are at the bottom of the page]...
items = ['TV', 'Camera', 'Projector', 'Walkman', 'Radio', 'Mobile phone', 'Laptop']
prices = [35, 85, 135, 10, 25, 2, 94]
kg = [2, 3, 9, 0.5, 2, 0.1, 4]
maxKg = 25


#The function we are trying to maximize...
def function_max(x):
    t = f_total_value(x)
    return t + f_total_kg(x, t)

#If we take all the items
def f_total_value(x):
    total = 0
    for i in range(len(x)):
        total += x[i] * prices[i]  # peice * price
    return total


def f_total_kg(x, reset_elem):
    total = 0
    for i in range(len(x)):
        total += x[i] * kg[i]  # piece * kg

    if total <= maxKg:
        if total <= reset_elem:
            return reset_elem - total
        else:
            return 0
    else:
        return - reset_elem

    """
        If kilogram exceeds maxKg;
        by returning the negative of the 1st function value as penalty point from the function,
        resets the result value so that it does not take the existing value...
    """



# Our particle class...
class Particle:
    def __init__(self, startingValues):
        self.position = []      # Particle position
        self.speed = []           # Particle speed
        self.pBest = []         # Individual best position
        self.pBestapproach = -1 # Individual best approach
        self.approach = -1      # individual approach

        for i in range(particles_number):
            self.speed.append(random.uniform(-1, 1))
            self.position.append(startingValues[i])

    # Calculate fitness for function...
    def calculate(self, function):
        self.approach = function(self.position)

        # Check if current position, Individual is best...
        if self.approach > self.pBestapproach or self.pBestapproach == -1:
            self.pBest = self.position
            self.pBestapproach = self.approach

    # Update new particle rate...
    def speed_update(self, group_max_position):
        w = 0.99    # The coefficient of the desire to maintain the previous velocity of the particle.
        c1 = 1.99   # The coefficient of the desire to protect her own best.
        c2 = 1.99   # Coefficient of willingness to get the best value of the swarm.

        for i in range(particles_number):
            r1 = random.random()
            r2 = random.random()

            individ_speed = c1 * r1 * (self.pBest[i] - self.position[i])
            social_speed = c2 * r2 * (group_max_position[i] - self.position[i])
            self.speed[i] = w * self.speed[i] + individ_speed + social_speed

    # Calculating new positions according to the newly updated particle velocity...
    def position_update(self, bounds):
        for i in range(particles_number):
            max_jump = (bounds[i][1] - bounds[i][0])

            if self.speed[i] < -max_jump:
                self.speed[i] = -max_jump
            elif self.speed[i] > max_jump:
                self.speed[i] = max_jump

            self.position[i] = self.position[i] + self.speed[i]

            if self.position[i] > bounds[i][1]:     # If position is above the upper limit value, pull to the upper limit value
                self.position[i] = bounds[i][1]
            elif self.position[i] < bounds[i][0]:    # If position is below the lower limit value, pull to the lower limit value

                self.position[i] = bounds[i][0]
            else:
                self.position[i] = round(self.position[i])

class PSO:
    curr_price, curr_kg, group_max_position, grupMaxapproach = [], [], [], -1

    def __init__(self, function, startingValues, bounds, piece_number, swarm_size, maxIter, printSteps = True): # function_max, startingValues, bounds, piece_number=7, maxIter=0.1
        global particles_number

        particles_number = len(startingValues)
        self.grupMaxapproach = -1  # Best approach for group
        self.group_max_position = []  # Best position for the group

        # Let's assign initial values ​​to our version...
        swarm = []
        for i in range(swarm_size):
            swarm.append(Particle(startingValues))

        # Optimization cycle start...
        counter = 0
        while counter < maxIter:
            counter += 1

            # Calculation of the functional suitability of the particles in the swarm...
            for j in range(swarm_size):
                swarm[j].calculate(function)

                # Checking whether the current thread is the global best and making the necessary updates...
                if swarm[j].approach > self.grupMaxapproach or self.grupMaxapproach == -1:
                    self.group_max_position = list(swarm[j].position)
                    self.grupMaxapproach = float(swarm[j].approach)

            # Updating the speed and positions in the herd...
            for j in range(swarm_size):
                swarm[j].speed_update(self.group_max_position)
                swarm[j].position_update(bounds)

            total_price = 0
            total_kg = 0
            for i in range(piece_number):
                total_price += self.group_max_position[i] * prices[i]
                total_kg += self.group_max_position[i] * kg[i]
            self.curr_price.append(total_price)
            self.curr_kg.append(total_kg)

            if printSteps:
                print(self.group_max_position)

    # Printing the results...
    def printResult(self):
        print('\n\nRESULTS:\n\n')
        total_price = 0
        total_kg = 0
        for i in range(len(self.group_max_position)):
            print(items[i], ': ', self.group_max_position[i], ' pcs', sep='')
            total_price += self.group_max_position[i] * prices[i]
            total_kg += self.group_max_position[i] * kg[i]
        print('#' * 50, '\nProfit Earned: ', total_price, ',\nKilogram: ', total_kg, sep='')

    # Plot the results to the screen [If we do not want to save the result image to the computer, the parameter named 'fileName' must be empty!]...
    def plotRes(self, fileName = ''):
        plt.plot(self.curr_kg, self.curr_price)
        plt.xlabel('Kilogram (kg)')
        plt.ylabel('Profit made')
        plt.title('Profit by Results - Kilogram Chart')
        plt.grid(True)

        if not(fileName == ''):        # If the variable 'fileName' is not empty, save the file with that name in png format...
            fileName = fileName+".png"
            plt.savefig(fileName)

        plt.show()
        plt.close()


# Assigning the starting and limit values ​​and running the algorithm...

# startingValues = [0, 0, 0, 0, 0, 0, 0]  # Baslangiç degerleri [x1, x2...]
# bounds = [(0, 12), (0, 8), (0, 2), (0, 50), (0, 12), (0, 250), (0, 6)]  # Sınır değerler [(x1_min,x1_max),(x2_min,x2_max)...]

print('[item_name: lower_qty - upper_qty]\n', sep='')
startingValues = []
bounds = []
for i in range(len(items)):
    startingValues.append(0)                                                    # Initial values ​​[x1, x2...]
    bounds.append((startingValues[i], math.floor(maxKg/kg[i])))          # Limit values ​​[(x1_min,x1_max),(x2_min,x2_max)...]
    print(items[i], ': ', bounds[i][0], ' - ', bounds[i][1], sep='')
print('\nincluding the total ', len(items), ' there is a variable...\n\n', sep='')

pso = PSO(function_max, startingValues, bounds, piece_number=len(items), swarm_size=100, maxIter=50, printSteps=True)
pso.printResult()
pso.plotRes(fileName='test')

# Algorithm end :)