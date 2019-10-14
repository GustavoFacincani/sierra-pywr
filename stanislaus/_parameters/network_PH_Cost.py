from parameters import WaterLPParameter


class network_PH_Cost(WaterLPParameter):
    """"""

    # path = "s3_imports/energy_netDemand.csv"

    def _value(self, timestep, scenario_index):

        demand_param = "node/" + self.res_name + "/Demand Constant"

        totDemand = self.model.parameters["Total Net Energy Demand"].value(timestep, scenario_index)
        maxDemand = self.model.parameters["Max Net Energy Demand"].value(timestep, scenario_index)
        minDemand = self.model.parameters["Min Net Energy Demand"].value(timestep, scenario_index)

        # data = self.read_csv(self.path, index_col=0, parse_dates=True)
        # totDemand, maxDemand, minDemand = data.loc[timestep.datetime]
        minVal = self.model.parameters[demand_param].value(timestep, scenario_index) * (
                totDemand / 768)  # 768 GWh is median daily energy demand for 2009
        maxVal = minVal * (maxDemand / minDemand)
        d = maxVal - minVal

        nblocks = self.model.parameters['Blocks'].value(timestep, scenario_index)
        return -(maxVal - ((self.block * 2 - 1) * d / 2) / nblocks)

    def value(self, timestep, scenario_index):
        return self._value(timestep, scenario_index)

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)

network_PH_Cost.register()

print(" [*] PH_Cost successfully registered")
