import random
import time
import buac_production.pbr_engine as pbr_engine
import buac_production.pbr_props as pbr_props
start_time = time.time()

filename = "aspen_1"
run_start_time = time.time()

count = 0
while count < 4:
    print '\nThe count is:', count
    pbr_props.show_info = True
    react_temp = random.uniform(pbr_props.temperature_lower_bound, pbr_props.temperature_upper_bound)
    react_pres = random.uniform(pbr_props.pressure_lower_bound, pbr_props.pressure_upper_bound)
    react_buoh = random.uniform(100, 500)
    react_acac = random.uniform(100, 500)
    print 'The temp is:', react_temp
    print 'The pressure is:', react_pres
    print 'The buoh is:', react_buoh
    print 'The acac is:', react_acac

    aspen_obj = pbr_engine.run(react_temp, react_pres, react_buoh, react_acac)
    aspen_obj.calculate_costs()
    aspen_obj.constraints_violations()
    count += 1

# aspen_obj = pbr_buac.run(110, 1.8, 250, 200)
# aspen_obj.calculate_costs()
# aspen_obj = pbr_buac.run(115, 1.8, 250, 200)
# aspen_obj.calculate_costs()
# aspen_obj = pbr_buac.run(110, 1.8, 300, 200)
# aspen_obj.calculate_costs()
# aspen_obj = pbr_buac.run(110, 1.8, 250, 300)
# aspen_obj.calculate_costs()
# aspen_obj = pbr_buac.run(110, 1.8, 150, 150)
# aspen_obj.calculate_costs()
# aspen_obj = pbr_buac.run(110, 1.1, 250, 200)
# aspen_obj.calculate_costs()
print("\n--- Simulation run: %s seconds ---" % (time.time() - run_start_time))
print("\n--- Whole run: %s seconds ---" % (time.time() - start_time))

pbr_engine.close_aspen()
