
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

NUMERIC_FEATURES = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
CATEGORICAL_FEATURES = ['Sex', 'Embarked']

def build_preprocessor():
    """Returns an unfitted ColumnTransformer handling all cleaning steps."""
    num_transformer = Pipeline([('imputer', SimpleImputer(strategy='median')),('scaler', StandardScaler())])

    cat_transformer = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),('onehot', OneHotEncoder(handle_unknown='ignore'))])  

    preprocessor = ColumnTransformer([('num', num_transformer, NUMERIC_FEATURES),('cat', cat_transformer, CATEGORICAL_FEATURES)])

    return preprocessor
