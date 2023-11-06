from math import exp, sqrt
from numpy.random import normal
import matplotlib.pyplot as plt


class PricingBinaryTree: 

    def __init__(self, ticker, dt, r, sigma, s0, n, K, option_type='call', discount='continuous'): 
        
        self.stock = ticker
        self.n = n # tree depth
        self.r = r # risk free interest rate 
        self.s = sigma # standard deviation for Bernstein/COx
        self.dt = dt
        self.s0 = s0
        self.u = exp(self.s*sqrt(self.dt))
        self.d = exp(-self.s*sqrt(self.dt))

        self.tree = self._tree_constructor()
        

        self.K = K
        self.option_type = option_type

        match self.option_type: 
            case 'call': 
                self.option = lambda x: max(0, x-self.K)
            case 'put':
                self.option = lambda x: max(0, self.K-x)
        self._leaf_initializer()
        
        self.dd = discount
        match discount: 
            case 'continuous': 
                self.discount = exp(-self.r*dt)
                self.pu = (exp(self.r)-self.d)/(self.u-self.d)
                self.pd = 1 - self.pu
            case 'simple': 
                self.discount = (1 + self.r)**-1
                self.pu = ((1+self.r-self.d)/(self.u - self.d))
                self.pd = 1 - self.pu
        
        if self.pu > 0 and self.pd < 0: 
            raise BaseException('Unacceptable parameters. Invalid probabilities.')
        

    def _tree_constructor(self, tree=[], j=1): 

        starting_point = int(j*(j+1)/2)
        ending_point = starting_point + j 

        if j == 1: 
            tree = [[self.s0, 'None']]    

        if j < self.n: 
            for i in range(starting_point,ending_point): 
                tree.append([tree[i-j][0]*self.u, 'None'])
                if i == ending_point - 1:
                    tree.append([tree[i-j][0]*self.d, 'None'])
            j +=1
            self._tree_constructor(tree=tree, j=j)
        
        return tree
    

    def _leaf_initializer(self): 

        for i in range(self.n): 
            self.tree[-self.n:][i][1] = self.option(self.tree[-self.n:][i][0])


    def european_option_price_dynamics(self, j):
        
        if j > 2:
            up_end = int((j-1)*j*0.5)
            low_end = int(up_end-(j-1))

            for i in range(low_end, up_end): 
                self.tree[i][1] = self.discount*(self.pu*self.tree[j-1+i][1] + self.pd*self.tree[j+i][1])
            j-=1
            self.european_option_price_dynamics(j)
        else:
            self.tree[0][1] = self.discount*(self.pu*self.tree[1][1] + self.pd*self.tree[2][1])
            self.european_option_price = self.tree[0][1]


    def american_option_price_dynamics(self, j):
        
        if j > 2:
            up_end = int((j-1)*j*0.5)
            low_end = int(up_end-(j-1))

            for i in range(low_end, up_end): 
                self.tree[i][1] = max(self.discount*(self.pu*self.tree[j-1+i][1] + self.pd*self.tree[j+i][1]), self.option(self.tree[i][0]))
            j-=1
            self.american_option_price_dynamics(j)
        else:
            self.tree[0][1] = max(self.discount*(self.pu*self.tree[1][1] + self.pd*self.tree[2][1]), self.option(self.tree[0][0])) 
            self.american_option_price = self.tree[0][1]


    def plot_results(self, data):

        fig, axs = plt.subplots(1, 2, figsize=(9,4))
        axs[0].plot(data)
        axs[0].set_xticks(axs[0].get_xticks())
        axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=25, ha='right')
        axs[0].grid()
        axs[0].set_title('Historical data for '+self.stock)
        axs[1].text(0.3, 1.0, f'{self.n}-steps interval:', fontsize=13)
        axs[1].text(0.3, 0.5, 'European '+self.option_type+f' : {self.european_option_price:.4}'+ '$', fontsize=12)
        axs[1].text(0.3, 0.6, 'American '+self.option_type+f' : {self.american_option_price:.4}'+ '$', fontsize=12)
        axs[1].text(0.3, 0.7, 'Discount type: '+self.dd, fontsize=12)
        axs[1].text(0.3, 0.8, f'Strike price {self.K}'+'$', fontsize=12)
        axs[1].spines['top'].set_visible(False)
        axs[1].spines['right'].set_visible(False)
        axs[1].spines['bottom'].set_visible(False)
        axs[1].spines['left'].set_visible(False)
        axs[1].set_xticks([])
        axs[1].yaxis.set_visible(False)
        plt.tight_layout()
        fig.show()
        plt.show()


    def print_results(self): 
        print('\n')
        print('#'*80)
        print('############### RESULTS ########################################################')
        print('#'*80)
        print('\n')
        print('Risk neutral probabilities: ', self.pu, ' ', self.pd)
        print('\n')
        print('Price of American ' + self.option_type +' option with given parameters: ', self.american_option_price)
        print('\n')
        print('Price of European ' + self.option_type +' option with given parameters: ', self.european_option_price)
        print('\n')
        print('#'*80)
        print('#'*80)
        print('\n')