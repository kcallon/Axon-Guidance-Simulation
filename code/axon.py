from environment import GridSquare, Environment
from typing import List, Tuple
class Axon:
    def __init__(self, comm_config, dcc_config, robo1_config, robo2_config) -> None:
        # TODO will need to build in setting the geneConfig with other configs - eventually
        self.geneConfig = {
            'COMM': comm_config, #True corresponds to Wildtype
            'DCC': dcc_config,
            'ROBO1': robo1_config,
            'ROBO2': robo2_config,
        }
        self.activatedGenes = {
            'COMM': True,
            'DCC': True,
            'ROBO1': False,
            'ROBO2': robo2_config,
        }
        self.ligandRewardWeights = {
            'netrin': 1,
            'slit': 1,
            'shh': 1,
            'targetLigand': 100
        }
        self.x = 0
        self.y = 0

        self.totalReward = 0
    
    

    def reward(self, slit, robo_wildtype, square: GridSquare) -> float:
        """given a GridSquare, use the activatedGenes to return the appropriate reward

        The reward is a linear combination of the ligand concentration * that ligand's weight 

        Returns:
            a float value of the reward
        """
        reward = 0
        print(self.activatedGenes['DCC'])
        print(self.activatedGenes['ROBO1'])
        print(self.activatedGenes['ROBO2'])
        print(self.activatedGenes['COMM'])
        if self.activatedGenes['DCC']:
            reward += self.ligandRewardWeights['netrin'] * square.netrin + \
                            self.ligandRewardWeights['shh'] * square.shh
        
        if self.activatedGenes['ROBO1'] and slit:
            reward += -1 * self.ligandRewardWeights['slit'] * square.slit

        reward += self.ligandRewardWeights['targetLigand'] * square.targetLigand

        return reward
    
    def modulateGenes(self, square: GridSquare):
        def ensureGeneConsistency() -> None:
            """Ensure that the genes are consistent with eachother
                Enforces the rule: COMM == not ROBO
                ROBO is default on 
            """
            if square.slit == 0 and not self.geneConfig['ROBO2'] and not self.activatedGenes['COMM']:
                self.activatedGenes['COMM'] = True

            if self.activatedGenes['COMM']:
                # send ROBO to the lysosome!
                self.activatedGenes['ROBO1'] = False
            else:
                self.activatedGenes['ROBO1'] = True
            
            # ensure that knocked-out genes are never set to True 
            for gene, value in self.geneConfig.items():
                if not value:
                    self.activatedGenes[gene] = False

        # axon behaves normally if ROBO2 is set to true
        if self.activatedGenes['ROBO1'] and square.slit > 0:
            self.activatedGenes['DCC'] = False

        if not self.geneConfig['ROBO2'] and square.slit == 0:
            self.activatedGenes['DCC'] = True
        # when first cross into midline, comm OFF
        if square.slit > 0 and self.geneConfig['COMM']:
            self.activatedGenes['COMM'] = False


        
        ensureGeneConsistency()

    def actions(self) -> List[Tuple]:
        return [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def getLegalMoves(self, env: Environment, x, y) -> List[Tuple]:
        actions = self.actions()

        #apply actions to x, y tuple
        potential_successors = []
        for action in actions:
            potential_successors.append(tuple([sum(tup) for tup in zip((x, y), action)]))
        
        #if any are outside of the bounds of the grid or have an axon already grown in them, get rid of them
        successors = [a for a in potential_successors if \
            env.inBounds(a[0], a[1], full = True) \
            and not env.getGridSquare(a[0], a[1], full=True).hasAxonShaft]
        return successors

    def chooseAction(self, env: Environment, x: int, y: int, verbose: bool =False):
        successors = self.getLegalMoves(env, x, y)
        rewards = [(i, self.reward(env.geneConfig['slit'], self.geneConfig['ROBO2'], env.getGridSquare(s[0], s[1], full=True))) for i, s in list(enumerate(successors))]
        max_reward = max(rewards, key=lambda x: x[1])
        max_reward_successor = successors[max_reward[0]]

        if verbose:
            print(f'cur location: {x}, {y}')
            print(f'sucessors: {successors}')
            print(f'rewards: {rewards}')
            print(f'choice: {max_reward_successor} reward: {max_reward[1]}')

        self.totalReward += max_reward[1]
        return max_reward_successor

    def chooseActionTurnLess(self, env: Environment, x: int, y: int, verbose: bool =False):
        def get4DirectionMoves(x, y):
            actions = self.actions()
            potential_successors = []
            for action in actions:
                potential_successors.append(tuple([sum(tup) for tup in zip((x, y), action)]))
            return [a for a in potential_successors if \
                    env.inBounds(a[0], a[1], full = True)]
        
        options = get4DirectionMoves(x, y)
        pass