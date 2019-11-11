from parameters import WaterLPParameter

from utilities.converter import convert

class node_IFR_bl_Bolsillo_Creek_Div_Requirement(WaterLPParameter):
    """"""

    def _value(self, timestep, scenario_index):
        return min(convert(0.4, 'ft^3 s^-1', 'hm^3 day^-1'), self.model.nodes["Bolsillo Creek Inflow [node]"].flow[-1])
        
    def value(self, timestep, scenario_index):
        return convert(self._value(timestep, scenario_index), "m^3 s^-1", "m^3 day^-1", scale_in=1, scale_out=1000000.0)

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)
        
node_IFR_bl_Bolsillo_Creek_Div_Requirement.register()
print(" [*] node_IFR_bl_Bolsillo_Creek_Div_Requirement successfully registered")
