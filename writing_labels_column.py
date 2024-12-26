import csv
import pandas as pd

# Function that adds a column to an existing CSV file.
def add_csv_column(file_name, column_name, column_values):
    
    # Read the content of the CSV file
    with open(file_name, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = list(csv.reader(csv_file))
        
        # Add the column name as a header
        if len(reader) > 0:
            reader[0].append(column_name)
        else:
            # If the file is empty, create only the header
            reader.append([column_name])
        
        # Add the column values
        for i, value in enumerate(column_values):
            if i + 1 < len(reader):
                reader[i + 1].append(value)
            else:
                # If there are more values than rows, add new rows
                new_row = [''] * (len(reader[0]) - 1) + [value]
                reader.append(new_row)

    # Write the updated content back to the CSV file
    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(reader)

# Main function
if __name__ == "__main__":
    csv_file_name = "labelled_dataset.csv"
    new_column_name = "label"
    dataset_size = 46
    values = []

    for i in range(dataset_size):
        if i in range(117):
            values.append("normal")
        elif i in range(118, 203):
            values.append("anomaly")
        elif i in range(204, 268):
            values.append("normal")
        elif i in range(269, 328):
            values.append("anomaly")
        elif i in range(329, 409):
            values.append("normal")
        elif i in range(410, 467):
            values.append("anomaly")
        else:
            values.append("normal")
    """
    for i in range(dataset_size):
        if i%2==0:
            values.append("normal")
        else:
            values.append("anomaly")
    """

    add_csv_column(csv_file_name, new_column_name, values)

    # Load file CSV
    df_new = pd.read_csv('labelled_dataset.csv')

    # Save file in Excel format
    df_new.to_excel('labelled_dataset.xlsx', index = False)
