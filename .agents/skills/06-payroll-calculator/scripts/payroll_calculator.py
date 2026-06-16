import pandas as pd
import os
import argparse

def calculate_payroll(input_file, output_file):
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"Reading data from {input_file.encode('utf-8', 'replace').decode('utf-8')}...")
    try:
        df = pd.read_excel(input_file)
        
        # Fill missing values with 0
        df['Base_Salary'] = df['Base_Salary'].fillna(0).astype(int)
        df['Bonus'] = df['Bonus'].fillna(0).astype(int)
        df['Penalty'] = df['Penalty'].fillna(0).astype(int)
        
        # Calculate Net Salary
        df['Net_Salary'] = df['Base_Salary'] + df['Bonus'] - df['Penalty']
        
        # Apply Zero-Floor Rule
        exceptions_count = (df['Net_Salary'] < 0).sum()
        df.loc[df['Net_Salary'] < 0, 'Net_Salary'] = 0
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write to excel
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Payroll_Cleaned')
        
        print(f"Success: Processed {len(df)} records.")
        print(f"Zero-Floor Rule applied to {exceptions_count} records.")
        print(f"Cleaned data saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing payroll data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate payroll from ERP data.')
    parser.add_argument('--input', type=str, required=True, help='Path to raw data excel file')
    parser.add_argument('--output', type=str, required=True, help='Path to output cleaned excel file')
    
    args = parser.parse_args()
    calculate_payroll(args.input, args.output)
