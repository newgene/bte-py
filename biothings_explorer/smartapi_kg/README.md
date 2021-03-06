[![Test](https://github.com/biothings/smartapi-kg.js/actions/workflows/test.yml/badge.svg)](https://github.com/biothings/smartapi-kg.js/actions/workflows/test.yml)
> Generate a meta knowledge graph of how biomedical concepts are connected based on SmartAPI Specifications with built-in filtering capabilities

### 🏠 [Homepage](https://github.com/kevinxin90/smartapi-kg.js#readme)

## Usage

- Import and Initialize

    ```python
    from biothings_explorer.smartapi_kg.metakg import MetaKG
    # initiate a new knowledge graph class
    meta_kg = MetaKG()
    ```

- Load the Meta Knowledge Graph (meta-kg)

  - Option 1: Load Meta-KG from SmartAPI specs with translator tag specified

    ```python
    # async load knowledge graph from SmartAPI
    meta_kg.construct_MetaKG()
    ```
  
  - Option 2: Load Meta-KG from SmartAPI specs with translator tag as well as ReasonerStdAPI with /predicates endpoint

    ```python
    meta_kg.construct_MetaKG(includeReasoner=True)
    ```
    
  - Option 3: Load Meta-KG from SmartAPI specs with tags equal to biothings

    ```python
    meta_kg.construct_MetaKG(includeReasoner = False, {"tag": "biothings"})
    ```
    
  - Option 4: Load Meta-KG from SmartAPI specs with team name equal to Text Mining Provider

    ```python
    meta_kg.construct_MetaKG(includeReasoner = False, {"teamName": "Text Mining Provider"})
    ```
  
  - Option 5: Load Meta-KG from SmartAPI specs with component equal to KP

    ```python
    meta_kg.construct_MetaKG(includeReasoner = False, {"component": "KP"})
    ```
    
  - Option 6: Load Meta-KG for a specific SmartAPI spec with SmartAPI ID

    ```python
    meta_kg.construct_MetaKG(includeReasoner = False, {"smartAPIID": "5076f09382b38d56a77e376416b634ca"})
    ```
    
  - Option 7: Load Meta-KG from a local copy of SmartAPI specs included in the package

    ```python
    # Alternatively, you can also sync load SmartAPI specs from a local copy within the package
    meta_kg.construct_MetaKG_sync()
    ```
    
  - Option 8: Load Meta-KG from file path you specify

    ```python
      import os
      # provide file path storing your SmartAPI file
      file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'smartapi_multiomics_kp_query.json'))
      meta_kg = MetaKG(file_path)
      meta_kg.construct_MetaKG_sync()
    ```
  
- Filter the Meta-KG for specific associations based on input, output, predicate, or api combinations.

    ```python
    # filter based on predicate
    meta_kg.filter({"predicate": 'treats'})
    # filter based on predicate and input_id
    meta_kg.filter({"predicate": 'treats', "input_id": 'CHEMBL.COMPOUND'})
    # filter based on predicate and input_type
    meta_kg.filter({"predicate": ['treats', 'physically_interacts_with'], "input_type": 'ChemicalSubstance'})
    # filter based on input_type, output_type and api
    meta_kg.filter({ "api": "Automat PHAROS API", "input_type": "ChemicalSubstance", "output_type": "Gene" })
