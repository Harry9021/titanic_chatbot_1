import pandas as pd
import os

def load_titanic_dataset():
    """
    Loads the Titanic dataset from local storage or downloads it if not available
    """
    data_path = os.path.join('app', 'data', 'titanic.csv')
    
    # Check if dataset already exists
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    
    # If not, download from a reliable source
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    
    # Save locally for future use
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    df.to_csv(data_path, index=False)
    
    return df

def get_dataset_info():
    """
    Returns basic information about the Titanic dataset
    """
    df = load_titanic_dataset()
    
    info = {
        "total_passengers": len(df),
        "survived_count": df['Survived'].sum(),
        "survival_rate": f"{(df['Survived'].mean() * 100):.2f}%",
        "features": list(df.columns),
        "missing_values": df.isnull().sum().to_dict()
    }
    
    return info

if __name__ == "__main__":
    # Test the function
    df = load_titanic_dataset()
    print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns")
    print(df.head())