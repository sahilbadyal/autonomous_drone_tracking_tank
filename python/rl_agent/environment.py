import gym
from gym import spaces
from env_config import *

class audrotrackEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self, data):
    super(audrotrackEnv, self).__init__()
    self.data = data
    # Define action and observation space
    # They must be gym.spaces objects
    # Example when using discrete actions:
    ## Represents the action along x and y directions
    self.reward_range = (-1.414*0.5 , 0)
    self.action_space = spaces.BOX(low=np.array([-1,-1], high=np.array([1,1])), dtype=np.float16)
    # Example for using image as input:
	## first 4 are centroids of the bounding box and image
	## Next are the controls given to the algorithm
    self.observation_space = spaces.Box(low=0, high=1, shape=
                    (1, 2), dtype=np.float16)

  def step(self, action):
    # Execute one time step within the environment
    #self._take_action(action)
    self.current_step += 1
    if self.current_step > len(self.data) - 1:
        self.current_step = 0
    reward = 
    obs = self._next_observation()
    return obs, reward, done, {}

  def reset(self):
    # Reset the state of the environment to an initial state
    self.current_step = -1

    return self._nextObservation()

  def _nextObservation(self):
      if self.current_step == -1:
          return np.array([0.5,0.5])
      obs = self.data[self.current_step][-2:]
      return obs

  #def _take_action(self):

