import math

# @memoization
class Biennial:
    """
    The baseline model assumes no density dependence for the plant
    and no larval competition in the stem

    """
    def __init__(self, initial_seedbank=None, probability_of_decay=None, probability_of_germination=None, maximum_plant_fecundity=None, fecundity_to_biomass=None, seedling_survival_to_flowering=None, seed_incorporation_rate=None, damage_function_shape=None, weevil_population=None, weevil_attack_rate=None, larval_survival=None, initial_flower_population=None, seedling_survival_to_rosette=None, initial_rosette_population=None, rosette_survival=None, average_seed_per_plant=None, conversion_coefficient=None, percent_increase_mortality=None):
        """
        set of parameters based on A. petiolata and C. scrobicollis
        """
        self.initial_seedbank = initial_seedbank or 400
        self.probability_of_decay = probability_of_decay or 0.35
        self.probability_of_germination = probability_of_germination or 0.13
        self.maximum_plant_fecundity = maximum_plant_fecundity or 200
        self.fecundity_to_biomass = fecundity_to_biomass or .025 # default for now. Equal to f(gsS(t-1) when there is no density dependence)
        self.seedling_survival_to_flowering = seedling_survival_to_flowering or 0.62
        self.seed_incorporation_rate = seed_incorporation_rate or 0.3
        self.damage_function_shape = damage_function_shape or .014
        self.weevil_population = weevil_population or 30
        self.weevil_attack_rate = weevil_attack_rate or .49  # percent reduction in seed
        self.larval_survival = larval_survival or 0.09 #made this up
        self.initial_flower_population = initial_flower_population or 40
        self.seedling_survival_to_rosette = seedling_survival_to_rosette or .54
        self.initial_rosette_population = initial_rosette_population or 100
        self.rosette_survival = rosette_survival or .62
        #self.average_seed_per_plant = average_seed_per_plant or 200
        self.conversion_coefficient = conversion_coefficient or 0.025 #conversion of plant matter to weevil's biomass? Need to run ECI for C. scrobicollis
        #self.percent_increase_mortality = percent_increase_mortality or 30

    def seedbank(self, gen):
        """
        The seedback is based on the sum of the seeds staying and new seeds.
        """
        if gen == 0:
            return self.initial_seedbank
        else:
            seeds_staying = ((1-self.probability_of_decay)*(1-self.probability_of_germination)*self.seedbank(gen-1))#breaking seedbank into two variables, probability they stay and probability new seeds enter
            new_seeds = self.flower(gen-1)*self.maximum_plant_fecundity*self.seed_incorporation_rate # * self.seed_recruitment_into_seedbank...look up seed_incorporation_rate
            return seeds_staying + new_seeds

    def rosette(self, gen):
        """
        rossetes are based on seeds that germinated in the current time step and survived to rosette
        """
        if gen == 0:
            return self.initial_rosette_population
        else:
            return self.probability_of_germination*self.seedling_survival_to_rosette*self.seedbank(gen)#((1-self.probability_of_decay)*self.seedbank(gen-1)*self.flower(gen-1)*self.maximum_plant_fecundity*self.seed_incorporation_rate)

    def flower(self, gen):
        """
        flower is based on proportion of rosettes that survived with the rate of attrition by weevil population
        """
        if gen == 0:
            return self.initial_flower_population
        else:
            return (self.rosette(gen-1)*self.rosette_survival)*math.e**(-(self.damage_function_shape*self.weevil_attack_rate*self.weevil(gen-1)/self.conversion_coefficient*self.maximum_plant_fecundity))#multiply by rate of attrition of weevil from Buckley

    def weevil(self, gen):
        """
        This weevil feeds on rosettes. Its population is based on rosettes of previous year
        another function can be added for a weevil that attacks another stage
        """
        if gen == 0:
            return self.weevil_population
        else:
            return self.rosette(gen-1)*self.weevil(gen-1)*self.weevil_attack_rate*self.larval_survival #*self.percent_increase_mortality)removed *self.probability_of_germination*self.seedling_survival_to_flowering

def make_biennial_table(): #loop for x amount of generations printing a row with numbers specified in make_biennial_row function
    b = Biennial()
    print(["y","S","R","F","W"])
    for y in range(18):
        print make_biennial_row(b, y)

def make_biennial_row(b, y):#print out biennial life table, will increase exponentially at this point
    S = b.seedbank(y)
    R = b.rosette(y)
    F = b.flower(y)
    W = b.weevil(y)
    return [y, int(round(S)), int(round(R)), int(round(F)), int(round(W))] #list will print as a row in make_biennial_table with gen, rosette number, and flower


if __name__ == '__main__':
    make_biennial_table()