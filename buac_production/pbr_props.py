"""
Performs the aspen PBR reactor simulation

Attributes:
    aspen                   COM object which links Python with Aspen Plus
    buac_production_goal    Molar flow of pruduced butyl acetate in kmol/h
"""
import math as m

# Parameters
buac_production_goal = 100  # in kmol/h

amberlyst15_price = 209  # USD/kg. Taken from https://www.alibaba.com/product-detail/CAS-9037-24-5-Amberlyst-15_60515092413.html. Or https://www.alfa.com/en/catalog/089079/
amberlyst15_density = 610  # g/l or kg/m**3. Taken from http://www.dow.com/assets/attachments/business/process_chemicals/amberlyst/amberlyst_15dry/tds/amberlyst_15dry.pdf
tube_inner_diameter = 1  # inches. TF http://elib.uni-stuttgart.de/bitstream/11682/1848/1/eig16.pdf (5mm)
tube_lewngth = 4  # Meters
tube_base_area = (tube_inner_diameter / 2.0 / 12.0) ** 2 * m.pi  # ft**2
acac_price = 560  # USD/ton. Taken from https://www.alibaba.com/product-detail/good-quality-low-price-Food-industry_60256609342.html
buoh_price = 1100  # USD/ton. Taken from https://www.alibaba.com/product-detail/N-Butanol-N-Butyl-Alcohol-Normal_60356088632.html
buoh_recovery = 0.99
acac_recovery = 0.99

# Properties
buoh_mw = 74.12  # kg/kmol
acac_mw = 60.05  # kg/kmol

# Variable Bounds
temperature_lower_bound = 50  # in Celsius
temperature_upper_bound = 120  # in Celsius
pressure_lower_bound = 1  # in bar
pressure_upper_bound = 10  # in bar
mole_flows_lower_bound = buac_production_goal  # in kmol/h
mole_flows_upper_bound = buac_production_goal * 5  # in kmol/h
bounds = [[temperature_lower_bound, pressure_lower_bound, mole_flows_lower_bound, mole_flows_lower_bound],
          [temperature_upper_bound, pressure_upper_bound, mole_flows_upper_bound, mole_flows_upper_bound]]

show_info = False

class PbrStatus:
    """
    Stores the main information of the simulation
    """

    def __init__(self, temperature_in, pressure, buoh_flow_in, acac_flow_in):
        self.in_temperature = temperature_in
        self.in_buoh_flow = buoh_flow_in
        self.in_acac_flow = acac_flow_in
        self.pressure = pressure

        self.out_buoh_flow = -1
        self.out_water_flow = -10
        self.out_acac_flow = -1
        self.out_buac_flow = -1
        self.out_vap_frac = -1
        self.out_temperature = -1
        self.catalyst_weight = -1
        self.catalyst_volume = -1

        self.capital_costs = -1
        self.losses_costs = -1
        self.constraints_count = -1

    def update_result(self, catalyst_weight, buoh_flow_out, water_flow_out, acac_flow_out, buac_flow_out, vap_fraction, temperature_out):
        self.out_buoh_flow = buoh_flow_out
        self.out_water_flow = water_flow_out
        self.out_acac_flow = acac_flow_out
        self.out_buac_flow = buac_flow_out
        self.out_vap_frac = vap_fraction
        self.out_temperature = temperature_out
        self.catalyst_weight = catalyst_weight
        self.catalyst_volume = catalyst_weight / amberlyst15_density  # m**3

        if show_info:
            print("\n--- buol out : %s kmol/h ---" % buoh_flow_out)
            print("--- acac out : %s kmol/h ---" % acac_flow_out)
            print("--- buac out : %s kmol/h ---" % buac_flow_out)
            print("--- water out : %s kmol/h ---" % water_flow_out)
            print("--- catalyst weight out : %s kg ---" % catalyst_weight)
            print("--- vapour fraction: %s ---" % vap_fraction)
            print("--- temperature out: %s ---" % temperature_out)


    def constraints_violations(self):
        constraints_count = 0
        # No vapour fraction
        if self.out_vap_frac > 0:
            constraints_count += 1
        # Butyl acetate production goal
        if self.out_buac_flow < buac_production_goal * 0.999:   # 0.01% of looseness
            constraints_count += 1
        # Temperature bounds
        if self.out_temperature < temperature_lower_bound or self.out_temperature > temperature_upper_bound:
            constraints_count += 1
        self.constraints_count = constraints_count
        if show_info:
            print("--- Violated constraints : %s ---" % constraints_count)

    def calculate_costs(self):
        surface_area = (self.catalyst_volume / (0.3048 ** 3)) / tube_base_area  # ft**2
        C_B = m.exp(11.0545 - 0.9228 * m.log(surface_area) + 0.09861 * (m.log(surface_area)) ** 2)
        FM = 2.7 + (surface_area / 100) ** 0.07
        self.capital_costs = (556.8 / 394.0) * C_B * FM * 1.05 + self.catalyst_weight * amberlyst15_price  # USD

        buoh_lost = self.out_buoh_flow * (1 - buoh_recovery)
        acac_lost = self.out_acac_flow * (1 - acac_recovery)
        self.losses_costs = buoh_lost * 24 * 330 * buoh_mw * buoh_price / 1000 + acac_lost * 24 * 330 * acac_mw * acac_price / 1000  # USD/yr
        if show_info:
            print("--- capital costs : %s ---" % self.capital_costs)
            print("--- operational costs : %s ---" % self.losses_costs)
