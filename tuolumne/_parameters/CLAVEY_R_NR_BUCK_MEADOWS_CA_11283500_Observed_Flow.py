from parameters import WaterLPParameter

from utilities.converter import convert

class CLAVEY_R_NR_BUCK_MEADOWS_CA_11283500_Observed_Flow(WaterLPParameter):
    """"""

    def _value(self, timestep, scenario_index):
        
        df = self.read_csv("Observed/Streamflow/GaugeStreamFlow_cms_TUO_R3.csv", index_col=0, header=0)
        return df["11283500"][timestep.datetime]
        
    def value(self, timestep, scenario_index):
        try:
            return convert(self._value(timestep, scenario_index), "m^3 s^-1", "m^3 day^-1", scale_in=1, scale_out=1000000.0)
        except Exception as err:
            print('ERROR for parameter {}'.format(self.name))
            print('File where error occurred: {}'.format(__file__))
            print(err)
            raise

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)
        
CLAVEY_R_NR_BUCK_MEADOWS_CA_11283500_Observed_Flow.register()
print(" [*] CLAVEY_R_NR_BUCK_MEADOWS_CA_11283500_Observed_Flow successfully registered")
