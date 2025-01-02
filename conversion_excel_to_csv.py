import pandas as pd

if __name__ == "__main__":
    # Load file Excel
    new_file = pd.read_excel("labelled_dataset.xlsx")

    # Save file in CSV format
    new_file.to_csv("labelled_dataset.csv", index = False)