import os
import pandas as pd

# Define directory and file path
output_dir = "new_examples"
file_path = os.path.join(output_dir, "sample_batch.csv")

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

# Define dataset with required deliberate edge cases
data = [
    # 1. Clean row for contrast
    {
        "PassengerId": 1001,
        "Survived": 0,
        "Pclass": 3,
        "Name": "Smith, Mr. John",
        "Sex": "male",
        "Age": 34.0,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": "A/5 21171",
        "Fare": 7.25,
        "Cabin": None,
        "Embarked": "S",
    },
    # 2. Blank Age
    {
        "PassengerId": 1002,
        "Survived": 1,
        "Pclass": 1,
        "Name": "Johnson, Mrs. Sarah",
        "Sex": "female",
        "Age": None,
        "SibSp": 1,
        "Parch": 0,
        "Ticket": "PC 17599",
        "Fare": 71.2833,
        "Cabin": "C85",
        "Embarked": "C",
    },
    # 3. Blank Embarked
    {
        "PassengerId": 1003,
        "Survived": 1,
        "Pclass": 3,
        "Name": "Williams, Miss. Mary",
        "Sex": "female",
        "Age": 26.0,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": "STON/O2. 3101282",
        "Fare": 7.925,
        "Cabin": None,
        "Embarked": None,
    },
    # 4. Sex capitalized as "Male"
    {
        "PassengerId": 1004,
        "Survived": 0,
        "Pclass": 1,
        "Name": "Brown, Mr. James",
        "Sex": "Male",
        "Age": 54.0,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": "113803",
        "Fare": 51.8625,
        "Cabin": "E46",
        "Embarked": "S",
    },
    # 5. Invalid Embarked port "X"
    {
        "PassengerId": 1005,
        "Survived": 0,
        "Pclass": 3,
        "Name": "Davis, Mr. William",
        "Sex": "male",
        "Age": 22.0,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": "370376",
        "Fare": 8.05,
        "Cabin": None,
        "Embarked": "X",
    },
    # 6. Fare as 0
    {
        "PassengerId": 1006,
        "Survived": 0,
        "Pclass": 2,
        "Name": "Miller, Mr. Edward",
        "Sex": "male",
        "Age": 38.0,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": "244373",
        "Fare": 0.0,
        "Cabin": None,
        "Embarked": "S",
    },
    # 7–10. Additional clean rows for contrast
    {
        "PassengerId": 1007,
        "Survived": 1,
        "Pclass": 2,
        "Name": "Wilson, Mrs. Ellen",
        "Sex": "female",
        "Age": 29.0,
        "SibSp": 1,
        "Parch": 0,
        "Ticket": "230433",
        "Fare": 26.0,
        "Cabin": None,
        "Embarked": "S",
    },
    {
        "PassengerId": 1008,
        "Survived": 0,
        "Pclass": 3,
        "Name": "Moore, Mr. Thomas",
        "Sex": "male",
        "Age": 19.0,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": "345778",
        "Fare": 8.05,
        "Cabin": None,
        "Embarked": "Q",
    },
    {
        "PassengerId": 1009,
        "Survived": 1,
        "Pclass": 1,
        "Name": "Taylor, Miss. Elizabeth",
        "Sex": "female",
        "Age": 35.0,
        "SibSp": 1,
        "Parch": 0,
        "Ticket": "113760",
        "Fare": 135.6333,
        "Cabin": "C123",
        "Embarked": "C",
    },
    {
        "PassengerId": 1010,
        "Survived": 0,
        "Pclass": 3,
        "Name": "Anderson, Mr. Peter",
        "Sex": "male",
        "Age": 45.0,
        "SibSp": 0,
        "Parch": 0,
        "Ticket": "347082",
        "Fare": 9.5,
        "Cabin": None,
        "Embarked": "S",
    },
]

# Convert to pandas DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv(file_path, index=False)

print(f"File successfully created at: {os.path.abspath(file_path)}")