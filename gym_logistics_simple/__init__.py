from gym.envs.registration import register

register(
  id='logistics-simple-v0',
  entry_point='gym_logistics_simple.envs:LogEnv'
)