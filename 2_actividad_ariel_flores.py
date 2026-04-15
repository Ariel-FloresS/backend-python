import pandas as pd 
from typing import Dict, Tuple, List



def load_excel_file(file_path:str)->Dict[str, pd.DataFrame]:

    """
    Load the Excel data from a 'file_path' and return a
    dictionary mapping Excel sheets to pandas Dataframes.
    """

    exported_data: Dict[str, pd.DataFrame] =  pd.read_excel(
                                                file_path,
                                                sheet_name = None  
                                            )

    return exported_data
                                            

def build_tables(excel_file_path:str)->Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    """
        Load and structure the main tables from the Excel file.

        This function reads the Excel file, extracts the base dataset,
        and builds separate catalog tables for: base de datos, entidad, egreso and enfermedad

    """

    excel_information: Dict[str, pd.DataFrame] = load_excel_file(file_path = excel_file_path)

    base_de_datos_table: pd.DataFrame = (excel_information['Base de datos']
                                        .filter(['ID','DIAS_ESTANCIA', 'EDAD',
                                                'GENERO', 'PESO', 'ALTURA', 'MES', 'ENTIDAD',
                                                'INDIGENA', 'MOTIVO_EGRESO', 'CODIGO_ENFERMEDAD'])
                                        .dropna(how = 'all')
                                        )


    catalogos: pd.DataFrame = excel_information['Catalogos']

    entidad_table: pd.DataFrame = (catalogos
                                    .filter(['ENTIDAD', 'NOMBRE_ENTIDAD'])
                                    .dropna(how = 'all')
                                )
    
    egreso_table: pd.DataFrame = (catalogos
                                    .filter(['MOTIVO_EGRESO', 'MOTIVO_EGRESO_DESC'])
                                    .dropna(how = 'all')
                                )

    enfermedades_table: pd.DataFrame = (catalogos
                                            .filter(['CODIGO_ENFERMEDAD', 'CODIGO_ENFERMEDAD_DESC'])
                                            .dropna(how = 'all')
                                        )

    return base_de_datos_table, entidad_table, egreso_table, enfermedades_table


def cleaning_steps_for_base_de_datos_table(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the main hospital dataset by applying basic data quality rules.

    This function:
    - Converts selected columns to the appropriate data types
    - Removes duplicated rows
    - Filters invalid values based on simple business rules
    
    Returns a cleaned base de datos dataframe.
    """
    # Data type conversion
    numeric_columns: List[str] = [
        'DIAS_ESTANCIA',
        'EDAD',
        'GENERO',
        'PESO',
        'ALTURA',
        'MES',
        'INDIGENA',
        'MOTIVO_EGRESO'
    ]

    for column in numeric_columns:
        dataset[column] = pd.to_numeric(dataset[column], errors='coerce')

    dataset['CODIGO_ENFERMEDAD'] = dataset['CODIGO_ENFERMEDAD'].astype('string')

    # Remove duplicated rows
    cleaned_dataset: pd.DataFrame = dataset.drop_duplicates()

    # Apply validation rules
    cleaned_dataset: pd.DataFrame = cleaned_dataset[cleaned_dataset['DIAS_ESTANCIA'] >= 0]

    cleaned_dataset: pd.DataFrame = cleaned_dataset[
        (cleaned_dataset['EDAD'] >= 0) & (cleaned_dataset['EDAD'] < 100)
    ]

    cleaned_dataset: pd.DataFrame = cleaned_dataset[cleaned_dataset['GENERO'].isin([1, 2])]

    cleaned_dataset: pd.DataFrame = cleaned_dataset[cleaned_dataset['PESO'] >= 0]

    cleaned_dataset: pd.DataFrame = cleaned_dataset[cleaned_dataset['ALTURA'] >= 0]

    cleaned_dataset: pd.DataFrame = cleaned_dataset[cleaned_dataset['MES'] >= 1]

    cleaned_dataset: pd.DataFrame = cleaned_dataset[cleaned_dataset['INDIGENA'].isin([1, 2, 9])]

    return cleaned_dataset

def enrich_base_dataset(fact_table: pd.DataFrame, 
                        entidad_catalog: pd.DataFrame,
                        egreso_catalog: pd.DataFrame,
                        enfermedad_catalog: pd.DataFrame)->pd.DataFrame:

    """
    Enrich the base dataset by joining it with the entity, discharge, and disease catalogs.

    This function merges the fact table with the corresponding catalog tables to replace
    coded values with their descriptive information, returning a dataset with enhanced context.
    """


    # data type conversion for enfermedad catalog
    enfermedad_catalog['CODIGO_ENFERMEDAD'] = enfermedad_catalog['CODIGO_ENFERMEDAD'].astype('string')


    enriched_base_dataset: pd.DataFrame = (
                            fact_table
                            .merge(entidad_catalog, on = 'ENTIDAD', how = 'left')
                            .merge(egreso_catalog, on = 'MOTIVO_EGRESO', how = 'left')
                            .merge(enfermedad_catalog, on = 'CODIGO_ENFERMEDAD', how = 'left')
                )
    enriched_base_dataset['INDIGENA'] = enriched_base_dataset['INDIGENA'].map({
                                                                    1: 'Indigena',
                                                                    2: 'No indigena',
                                                                    9: 'No se sabe'
                                                                })

    enriched_base_dataset['GENERO'] = enriched_base_dataset['GENERO'].map({
                                                                    1: 'Masculino',
                                                                    2: 'Femenino'
                                                                })
    return enriched_base_dataset




def generate_basic_stats(big_one_table:pd.DataFrame)->None:

    """
    Displays statistical information about the big one table
    """

    print("\n===== BASIC DATA OVERVIEW =====")
    print(f"Total number of records: {len(big_one_table)}")

    print("\n===== NUMERICAL STATISTICS =====")
    print(big_one_table[['EDAD', 'PESO', 'ALTURA', 'DIAS_ESTANCIA']].describe())

    print("\n===== DISTRIBUTION: GENERO =====")
    print(big_one_table['GENERO'].value_counts())

    print("\n===== DISTRIBUTION: INDIGENA =====")
    print(big_one_table['INDIGENA'].value_counts())

    print("\n===== TOP 5 ENTITIES =====")
    print(big_one_table['NOMBRE_ENTIDAD'].value_counts().head(5))

    print("\n===== TOP 5 DISEASES =====")
    print(big_one_table['CODIGO_ENFERMEDAD_DESC'].value_counts().head(5))

    print("\n===== TOP 5 DISCHARGE REASONS =====")
    print(big_one_table['MOTIVO_EGRESO_DESC'].value_counts().head(5))

    print("\n===== PATIENTS COUNT BY ENTITY =====")
    print(big_one_table.groupby('NOMBRE_ENTIDAD')['ID'].count().sort_values(ascending=False).head(5))




def save_dataframe_to_parquet(dataset: pd.DataFrame, output_path: str) -> None:
    """
    Save a pandas DataFrame to a Parquet file.
    """
    dataset.to_parquet(output_path, engine='pyarrow', index=False)



def main()->None:

    
    
    excel_file_path: str = 'Hospitales.xlsx'

    save_path: str = 'consolidate_hospitales_information.parquet'

    

    # Load Fact table (base de datos) and Catalogs
    fact_table, entidad_catalog, egreso_catalog, enfermedad_catalog = build_tables(excel_file_path = excel_file_path)

    # Cleaning fact table
    cleaned_fact_table: pd.DataFrame = cleaning_steps_for_base_de_datos_table(dataset = fact_table)

    # Mergin catalogs with the fact table
    big_one_table: pd.DataFrame = enrich_base_dataset(fact_table = cleaned_fact_table,
                                                    entidad_catalog = entidad_catalog,
                                                    egreso_catalog = egreso_catalog,
                                                    enfermedad_catalog = enfermedad_catalog
                                                    )

    # basic stadistics values
    generate_basic_stats(big_one_table = big_one_table)

    # persist the big one table 
    save_dataframe_to_parquet(dataset = big_one_table, output_path = save_path)

    

if __name__=='__main__':

    main()