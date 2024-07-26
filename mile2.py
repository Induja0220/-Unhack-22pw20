import pandas as pd
import math

# Load data from CSV files
care_areas = pd.read_csv('CareAreas.csv', names=['id', 'x1', 'x2', 'y1', 'y2'])
metadata = pd.read_csv('metadata.csv', names=['main_field_side', 'sub_field_side'], skiprows=1)
main_field_side = int(metadata['main_field_side'].values[0])
sub_field_side = int(metadata['sub_field_side'].values[0])

# Calculate area and number of subareas
care_areas['area'] = (care_areas['x2'] - care_areas['x1']) * (care_areas['y2'] - care_areas['y1'])
care_areas['nosubarea'] = care_areas['area'].apply(lambda a: math.ceil(a / (sub_field_side * sub_field_side)))

main_fields = []
j = 0

# Main field
for i in range(len(care_areas)):
    x1, x2, y1, y2 = care_areas.iloc[i, 1], care_areas.iloc[i, 2], care_areas.iloc[i, 3], care_areas.iloc[i, 4]
    if i == 0 or x2 > main_field_side + fx1 or y2 > main_field_side + fy1:
        main_fields.append([j, x1, x1 + main_field_side, y1, y1 + main_field_side])
        fx1, fx2 = x1, x1 + main_field_side
        fy1, fy2 = y1, y1 + main_field_side
        j += 1

# Calculate subfields
sub_fields = []
sub_field_id = 0

for mf in main_fields:
    _, mf_x1, mf_x2, mf_y1, mf_y2 = mf
    for i, row in care_areas.iterrows():
        x1, x2, y1, y2 = row['x1'], row['x2'], row['y1'], row['y2']
        sub_x_steps = math.ceil((x2 - x1) / sub_field_side)
        sub_y_steps = math.ceil((y2 - y1) / sub_field_side)
        for sx in range(sub_x_steps):
            for sy in range(sub_y_steps):
                sf_x1 = x1 + sx * sub_field_side
                sf_y1 = y1 + sy * sub_field_side
                sf_x2 = min(sf_x1 + sub_field_side, x2)
                sf_y2 = min(sf_y1 + sub_field_side, y2)
                if sf_x1 >= mf_x1 and sf_x2 <= mf_x2 and sf_y1 >= mf_y1 and sf_y2 <= mf_y2:
                    sub_fields.append([sub_field_id, sf_x1, sf_x2, sf_y1, sf_y2])
                    sub_field_id += 1

# Convert to DataFrame and save to CSV
main_fields_df = pd.DataFrame(main_fields, columns=['id', 'x1', 'x2', 'y1', 'y2'])
sub_fields_df = pd.DataFrame(sub_fields, columns=['id', 'x1', 'x2', 'y1', 'y2'])

main_fields_df.to_csv('mainfields.csv', index=False)
sub_fields_df.to_csv('subfields.csv', index=False)
