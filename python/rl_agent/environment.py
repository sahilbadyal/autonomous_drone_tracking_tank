import gym
from gym import spaces
from env_config import *

class audrotrackEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self, data):
    super(CustomEnv, self).__init__()
    self.data = data
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    ## Represents the action along x and y directions
    self.reward_range = (0, MAX_REWARD)
    self.action_space = spaces.BOX(low=np.array([-1,-1], high=np.array([1,1])), dtype=np.float16)
    # Example for using image as input:
	## first 4 are centroids of the bounding box and image
	## Next are the controls given to the algorithm
    self.observation_space = spaces.Box(low=0, high=1, shape=
                    (1, 10), dtype=np.uint8)

  def step(self, action):
    # Execute one time step within the environment
    raise NotImplementedError()

  def reset(self):
    # Reset the state of the environment to an initial state
    raise NotImplementedError()

