"""
Настройка эксперимента записи и тюнинга
"""

import json
from manager.service import r2a
from manager import Manager

def get_result_file_name(min_res, max_res):
    return f'{min_res}_{max_res}_tuning_10.json' # путь к файлу эксперимента записи и тюнинга, где min_res и max_res - минимальное и максимальное сопротивление соответственно

min_res = [9000,5000] # список минимальных сопротивлений для эксперимента записи и тюнинга
max_res = [10000,6000] # список максимальных сопротивлений для эксперимента записи и тюнинга
filepath = 'write_template.json' # путь к файлу шаблона для эксперимента записи и тюнинга

man = Manager()
with open (filepath, "r+") as f:
    data = f.read()
tickets = json.loads(data)

for i in range(len(min_res)):
    center_conductance = (1/min_res[i]+1/max_res[i])/2
    center_resistance = int(1/center_conductance)
    print(min_res[i], center_resistance, max_res[i])

    for item in tickets:
        if tickets[item]["terminate"]['type'] == "><":
            min_adc = r2a(man.gain,
                        man.res_load,
                        man.vol_read,
                        man.adc_bit,
                        man.vol_ref_adc,
                        man.res_switches,
                        max_res[i])
            max_adc = r2a(man.gain,
                        man.res_load,
                        man.vol_read,
                        man.adc_bit,
                        man.vol_ref_adc,
                        man.res_switches,
                        min_res[i])
            tickets[item]["terminate"]['value'] = [min_adc, max_adc]
        elif tickets[item]["terminate"]['type'] in ["<", ">"]:
            center_adc = r2a(man.gain,
                        man.res_load,
                        man.vol_read,
                        man.adc_bit,
                        man.vol_ref_adc,
                        man.res_switches,
                        center_resistance)
            tickets[item]["terminate"]['value'] = center_adc

    with open(get_result_file_name(min_res[i], max_res[i]), 'w+', encoding='utf-8') as outfile:
        outfile.write("{")
        for i in range(len(tickets)):
            outfile.write('"' + str(i) + '":')
            json.dump(tickets[str(i)], outfile)
            if i < len(tickets)-1:
                outfile.write(",\n")
        outfile.write("}")
