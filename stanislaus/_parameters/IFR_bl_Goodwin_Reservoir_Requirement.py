import datetime
import numpy as np
from parameters import WaterLPParameter

from utilities.converter import convert

from dateutil.relativedelta import relativedelta


class IFR_bl_Goodwin_Reservoir_Requirement(WaterLPParameter):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            swrcb_levels_count = self.model.scenarios['SWRCB 40'].size
            if swrcb_levels_count == 1:
                self.swrcb_levels = [0.0]  # baseline scenario only
            else:
                self.swrcb_levels = np.arange(0.0, 0.41, 0.4 / (swrcb_levels_count - 1))
        except:
            # print("SWRCB 40 scenario doesn't exist.")
            pass

    def _value(self, timestep, scenario_index):
        WYT = self.get('San Joaquin Valley WYT' + self.month_suffix)
        schedule = self.model.tables["IFR bl Goodwin Dam schedule"]
        start = '{}-{}'.format(self.datetime.month, self.datetime.day)
        if self.model.mode == 'scheduling':
            min_ifr = schedule.at[start, WYT] / 35.31  # cfs to cms
            # min_ifr = self.get_down_ramp_ifr(timestep, scenario_index, min_ifr, initial_value=200 / 35.31, rate=0.02)
            if self.datetime.day in (1, 15):
                min_ifr = self.get_down_ramp_ifr(timestep, scenario_index, min_ifr, initial_value=200 / 35.31, rate=0.25)
            elif timestep.index > 0:
                min_ifr = self.model.nodes[self.res_name].prev_flow[-1] / 0.0864

        else:
            end = '{}-{}'.format(self.datetime.month, self.days_in_month())
            min_ifr = schedule[WYT][start:end].mean() / 35.31  # cfs to cms

        # SCWRB 40 REQUIREMENT
        if 2 <= timestep.month <= 7 and scenario_index:
            try:
                fnf = self.model.tables['Full Natural Flow'][self.datetime]
                swrcb_reqt_cms = fnf * self.swrcb_levels[scenario_index.indices[0]] / 0.0864 # mcm to cms
                min_ifr = max(min_ifr, swrcb_reqt_cms)
            except:
                pass

        return min_ifr

    def value(self, timestep, scenario_index):
        try:
            return convert(self._value(timestep, scenario_index), "m^3 s^-1", "m^3 day^-1", scale_in=1,
                           scale_out=1000000.0)
        except Exception as err:
            print('\nERROR for parameter {}'.format(self.name))
            print('File where error occurred: {}'.format(__file__))
            print(err)

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)


IFR_bl_Goodwin_Reservoir_Requirement.register()
print(" [*] IFR_bl_Goodwin_Reservoir_Requirement successfully registered")
