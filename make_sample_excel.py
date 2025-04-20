import pandas as pd
import random
import os

# Create directory if doesn't exist
os.makedirs("static/uploads", exist_ok=True)

# Generate 50 random Iranian mobile numbers
mobile_numbers = []
for _ in range(50):
    # Iranian mobile numbers typically start with 09
    number = "09"
    # Add 9 more random digits
    for _ in range(9):
        number += str(random.randint(0, 9))
    mobile_numbers.append(number)

# Create a dataframe with the mobile numbers
df = pd.DataFrame({
    "نام": [f"شرکت کننده {i+1}" for i in range(50)],
    "شماره موبایل": mobile_numbers
})

# Save to Excel file
file_path = "static/uploads/sample_participants.xlsx"
df.to_excel(file_path, index=False)

print(f"Sample Excel file created at: {file_path}") 