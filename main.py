import pickle
import pygame
from GameComponents.Game import Game
import neat 
import numpy as np
pygame.init()

class AI:
    def __init__(self, width,height,fps,config= None):
        self.config = config
        
        self.width = width
        self.height = height
        self.fps = fps
        self.game = Game(self.width,self.height)
        
        self.active_clock = True
        
        self.number_of_moves = 200
        self.max_moves = 500
        self.alive = 0
        self.clock = pygame.time.Clock()
        
    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.snake.change_direction([1,0,0])
                elif event.key == pygame.K_DOWN:
                    self.game.snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.game.snake.change_direction([0,0,1])
                elif event.key == pygame.K_RIGHT:
                    self.game.snake.change_direction([0,1,0])
                if event.key == pygame.K_a:
                    self.active_clock  = True
            
        return True

    def handle_AI_action(self,action:int) ->None:
        if action == 0:
            self.game.snake.change_direction('UP')
        elif action == 1:
            self.game.snake.change_direction('DOWN')
        elif action == 2:
            self.game.snake.change_direction('LEFT')
        elif action == 3:
            self.game.snake.change_direction('RIGHT')
    
    

    def test_AI(self, genome = None):

        #net = neat.nn.FeedForwardNetwork.create(genome, self.config)

        clock = pygame.time.Clock()
        # Set up the game loop
        running = True
        
        while running:
            clock.tick(self.fps)
            running = self.handle_events()

            # Get inputs from the game state
            #inputs = [i for i in range(0,24)]
            # Use the neural network to get the output
            #output = net.activate(inputs)
            # Convert the output to an action
            #action = np.argmax(output)
            
            #self.handle_AI_action(action)

            # Update the game state
            self.game.snake.move()
            lost = self.game.check_snake_body_collision() or self.game.check_snake_wall_collision()
            
            self.game.check_snake_food_collision()
            #print(self.game.Sensors.get_neuralNetwork_input())
            print(self.game.Sensors.get_neuralNetwork_input())
            if lost:
                self.game.game_over()
            # Draw the game
            self.game.draw(
                draw_sensor=True,
                )
            pygame.display.update()
            # Wait for the next frame if you activated the clock
            

    def increase_moves(self):
        if self.number_of_moves+100<self.max_moves:
            self.number_of_moves+= 100
        else:
            self.number_of_moves = self.number_of_moves

    def train_AI(self,genome,draw = False):
        
        net = neat.nn.FeedForwardNetwork.create(genome, self.config)
    
        running = True
        
        while running:
            running = self.handle_events()
            
            if not running:
                quit()
            
            
            inputs = self.game.Sensors.get_neuralNetwork_input()
            
            output = net.activate(inputs)
            # Convert the output to an action
            action = np.argmax(output)

            self.handle_AI_action(action)
            
            self.game.snake.move()
            self.alive += 1
            self.number_of_moves -= 1
            
            lost = self.game.check_octcale_collisions()

            gain = self.game.check_food_collision()
            
            if draw :
                self.game.draw(
                draw_sensor=True 
                )
                pygame.display.update()
            
            if lost or self.number_of_moves <=0:
                genome.fitness -= 5
                self.calc_fitness(genome)
                self.game.game_over()
                break
            
            if gain:
                self.increase_moves()
                
            
            if self.active_clock:
                self.clock.tick(self.fps)
            
        
    def calc_fitness(self,genome):
        genome.fitness += self.game.score.get_score() *3

        if self.number_of_moves <= 0:
            genome.fitness += 0.5
        else:
            genome.fitness -= (1)
            genome.fitness += self.alive / 100.0
            
            

def eval_genomes(genomes, config):
    width, height = 640, 480
    fps = 20
    for _, genome in genomes:
        genome.fitness = 0
        ai = AI(config,width,height,fps)
        ai.train_AI(genome,draw = True)

def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-198')
    # Create a new population of genomes with the given configuration
    #p = neat.Population(config)
    
    # Add a StdOutReporter to print statistics to the console
    p.add_reporter(neat.StdOutReporter(True))
    
    # Add a StatisticsReporter to collect statistics on the population
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    # Add a Checkpointer to save the population every 1 generation
    p.add_reporter(neat.Checkpointer(1))
    
    # Run the population for 50 generations and return the winning genome
    winner = p.run(eval_genomes, 50)
    
    # Save the winning genome to a pickle file
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

# if __name__ == '__main__':
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, 'config.txt')
#     config= neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                         config_path)
#     run_neat(config)

width, height = 640, 480
fps = 20
ai = AI(width,height,fps)
ai.test_AI()
