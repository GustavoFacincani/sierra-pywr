from parameters import WaterLPParameter

from utilities.converter import convert

class Cherry_Lake_Humidity(WaterLPParameter):
    """"""

    def _value(self, timestep, scenario_index):
        kwargs = dict(timestep=timestep, scenario_index=scenario_index)
        path="{ExternalDir}/{Scenario}/Climate/TUO_10_Humidity.csv".format(ExternalDir=self.GET("network/1237/1594", **kwargs), Scenario=self.GET("network/1237/1595", **kwargs))
        data = self.read_csv(path, usecols=[0,1,2], comment=';', header=None, **kwargs)
        return data.iloc[timestep][2]
        
    def value(self, timestep, scenario_index):
        try:
            return self._value(timestep, scenario_index)
        except Exception as err:
            print('ERROR for parameter {}'.format(self.name))
            print('File where error occurred: {}'.format(__file__))
            print(err)
            raise

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)
        
Cherry_Lake_Humidity.register()
print(" [*] Cherry_Lake_Humidity successfully registered")
