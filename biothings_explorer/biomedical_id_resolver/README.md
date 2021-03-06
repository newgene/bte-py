# biomedical_id_resolver.py
python library for resolving biological ids to their equivalent ids in batch

## Usage

```python
from biothings_explorer.biomedical_id_resolver.resolver import Resolver
resolver = Resolver()

# input should be an object, with semantic type as the key, and array of CURIEs as value
_input = {
    "Gene": ["NCBIGene:1017", "NCBIGene:1018", "HGNC:1177"],
    "ChemicalSubstance": ["CHEBI:15377"],
    "Disease": ["MONDO:0004976"],
    "Cell": ["CL:0002372"]
  }

print(resolver.resolve(_input))
# => {'NCBIGene:1017': {...}, 'NCBIGene:1018': {...}, 'HGNC:1177': {...}, 'CHEBI:15377': {...}, 'MONDO:0004976': {...}, 'CL:0002372': {...}}
```

## Output Schema

- Output is a python Object

- The root keys are CURIES (e.g. NCBIGene:1017) which are passed in as input

- The values represents resolved identifiers

- Each CURIE will have 4 required fields

  - id: the primary id (selected based on the ranking described in the next section) and label

  - curies: an array, each element represents a resolved id in CURIE format

  - type: the semantic type of the identifier

  - db_ids: original ids from source database, could be curies or non-curies.


- if an ID can not be resolved using the package, it will have an additional field called "flag", with value equal to "failed"

- Example Output

```json
{
  "NCBIGene:1017": {
    "id": {
      "label": "cyclin dependent kinase 2",
      "identifier": "NCBIGene:1017"
    },
    "db_ids": {
      "NCBIGene": [
        "1017"
      ],
      "ENSEMBL": [
        "ENSG00000123374"
      ],
      "HGNC": [
        "1771"
      ],
      "SYMBOL": [
        "CDK2"
      ],
      "UMLS": [
        "C1332733",
        "C0108855"
      ],
      "name": [
        "cyclin dependent kinase 2"
      ]
    },
    "type": "Gene",
    "curies": [
      "NCBIGene:1017",
      "ENSEMBL:ENSG00000123374",
      "HGNC:1771",
      "SYMBOL:CDK2",
      "UMLS:C1332733",
      "UMLS:C0108855"
    ]
  }
}
```

## Available Semantic Types & prefixes

> Gene ID resolution is done through MyGene.info API

- Gene
  1. NCBIGene
  2. ENSEMBL
  3. HGNC
  4. SYMBOL
  5. OMIM
  6. UniProtKB
  7. UMLS
  8. name

> Variant ID resolution is done through MyVariant.info API

- SequenceVariant
  1. HGVS
  2. DBSNP
  3. MYVARIANT_HG19
  4. ClinVar

> ChemicalSubstance ID resolution is done through MyChem.info API

- ChemicalSubstance
    1. CHEBI
    2. CHEMBL.COMPOUND
    3. DRUGBANK
    4. PUBCHEM
    5. MESH
    6. INCHI
    7. INCHIKEY
    8. UNII
    9. KEGG
    10. UMLS
    11. name
    12. id

> Disease ID Resolution is done through MyDisease.info API

- Disease

  1. MONDO
  2. DOID
  3. OMIM
  4. ORPHANET
  5. EFO
  6. UMLS
  7. MESH
  8. GARD
  9. name

> Pathway ID Resolution is done through biothings.ncats.io/geneset API

- Pathway
  1. Reactome
  2. KEGG
  3. PHARMGKB
  4. WIKIPATHWAYS
  5. name

> MolecularActivity ID Resolution is done through BioThings Gene Ontology Molecular Activity API

- MolecularActivity
  1. GO
  2. MetaCyc
  3. RHEA
  4. KEGG.REACTION
  5. Reactome

> CellularComponent ID Resolution is done through BioThings Gene Ontology Cellular Component API

- CellularComponent
  1. GO
  2. MESH
  3. UMLS
  4. NCIT
  5. SNOMEDCT
  6. UBERON
  7. CL
  8. name

> BiologicalProcess ID Resolution is done through BioThings Gene Ontology Biological Process API

- BiologicalProcess

  1. GO
  2. MetaCyc
  3. Reactome
  4. name

> AnatomicalEntity ID Resolution is done through BioThings UBERON API

- AnatomicalEntity
  1. UBERON
  2. UMLS
  3. NCIT
  4. MESH
  5. name

> PhenotypicFeature ID Resolution is done through BioThings HPO API

- PhenotypicFeature
  1. UMLS
  2. SNOMEDCT
  3. HP
  4. MEDDRA
  5. EFO
  6. NCIT
  7. MESH
  8. MP
  9. name

> Cell ID Resolution is done through nodenormalization API

- Cell
  1. CL
  2. UMLS
  3. NCIT
  4. MESH
  5. UBERON
  6. SNOMEDCT
  7. name
