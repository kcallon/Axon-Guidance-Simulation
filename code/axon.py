from environment import GridSquare, Environment
class Axon:
    def __init__(self) -> None:
        # will need to build in setting the geneConfig with other configs - eventually
        self.geneConfig = {
            'COMM': True,
            'DCC': True,
            'ROBO': True,
        }
        self.activatedGenes = {
            'COMM': True,
            'DCC': True,
            'ROBO': False,
        }
        self.x = 0
        self.y = 0
    
    def ensureGeneConsistency(self) -> None:
        """Ensure that the genes are consistent with eachother
            Enforces the rule: COMM == not ROBO
            ROBO is default on 
        """
        if self.activatedGenes['COMM']:
            # send ROBO to the lysosome!
            self.activatedGenes['ROBO'] = False
        else:
            self.activatedGenes['ROBO'] = True
        
        # ensure that knocked-out genes are never set to True 
        for gene, value in self.geneConfig:
            if not value:
                self.activatedGenes[gene] = False

    def reward(self, square: GridSquare) -> float:
        """given a GridSquare, use the activatedGenes to return the appropriate reward

        Returns:
            a float value of the reward
        """
        if self.activatedGenes['DCC']:
            return square.netrin + square.shh
        
        if self.activatedGenes['ROBO']:
            return -1 * square.slit
    
    def modulateGenes(self, square: GridSquare): 
        
        if self.activatedGenes['ROBO'] and square.slit > 0:
            self.activatedGenes['DCC'] = False
        
        # when first cross into midline, comm OFF
        if square.slit > 0: 
            self.activatedGenes['COMM'] = False
        
        self.ensureGeneConsistency()

    