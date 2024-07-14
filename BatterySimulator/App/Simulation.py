import pybamm
from pydantic import BaseModel, validator

from BatterySimulator.App.Model import ConfigModel
from BatterySimulator.App.Solver import ConfigSolver

class BaseSimulation(BaseModel):
    config_model: ConfigModel
    config_solver: ConfigSolver

    def construct_simulation_model(self):
        model = self.config_model.set_electrochemical_model()
        parameter_values = self.config_model.set_bpx_model()
        solver = self.config_solver.set_solver()

        simulation_model = {
            "model": model,
            "parameter_values": parameter_values,
            "solver": solver
        }
        return simulation_model

class TimeEvaluationSimulation(BaseSimulation):
    t_eval: list

    def simulate(self):
        simulation_model = self.construct_simulation_model()

        sim = pybamm.Simulation(model=simulation_model["model"],
                                parameter_values=simulation_model["parameter_values"],
                                solver=simulation_model["solver"])
        
        sim.solve(self.t_eval)
        sim.plot()