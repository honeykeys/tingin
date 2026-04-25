from openreward.environments import Server
from tingin_env.environment import NursingHandoffEnv

if __name__ == "__main__":
    Server([NursingHandoffEnv]).run()
