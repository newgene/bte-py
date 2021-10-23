CURIE = {
    "ALWAYS_PREFIXED": ['RHEA', 'GO', 'CHEBI', 'HP', 'MONDO', 'DOID', 'EFO', 'UBERON', 'MP', 'CL', 'MGI'],
}

TIMEOUT = 30000

MAX_BIOTHINGS_INPUT_SIZE = 1000

MAX_CONCURRENT_QUERIES = 3

APIMETA = {
  "Gene":{
    "id_ranks":[
      "NCBIGene",
      "ENSEMBL",
      "HGNC",
      "MGI",
      "OMIM",
      "UMLS",
      "SYMBOL",
      "UniProtKB",
      "name"
    ],
    "semantic":"Gene",
    "api_name":"mygene.info",
    "url":"https://mygene.info/v3/query",
    "mapping":{
      "NCBIGene":[
        "entrezgene"
      ],
      "name":[
        "name"
      ],
      "SYMBOL":[
        "symbol"
      ],
      "UMLS":[
        "umls.cui",
        "umls.protein_cui"
      ],
      "HGNC":[
        "HGNC"
      ],
      "UniProtKB":[
        "uniprot.Swiss-Prot"
      ],
      "ENSEMBL":[
        "ensembl.gene"
      ],
      "OMIM":[
        "MIM"
      ],
      "MGI":[
        "MGI"
      ]
    },
    "additional_attributes_mapping":{
      "interpro":[
        "interpro.desc"
      ],
      "type_of_gene":[
        "type_of_gene"
      ]
    }
  },
  "Transcript":{
    "id_ranks":[
      "ENSEMBL",
      "SYMBOL",
      "name"
    ],
    "semantic":"Transcript",
    "api_name":"mygene.info",
    "url":"https://mygene.info/v3/query",
    "mapping":{
      "ENSEMBL":[
        "ensembl.transcript"
      ],
      "SYMBOL":[
        "symbol"
      ],
      "name":[
        "name"
      ]
    },
    "additional_attributes_mapping":{
      "interpro":[
        "interpro.desc"
      ]
    }
  },
  "Protein":{
    "id_ranks":[
      "UniProtKB",
      "ENSEMBL",
      "UMLS",
      "SYMBOL",
      "name"
    ],
    "semantic":"Protein",
    "api_name":"mygene.info",
    "url":"https://mygene.info/v3/query",
    "mapping":{
      "name":[
        "name"
      ],
      "SYMBOL":[
        "symbol"
      ],
      "UMLS":[
        "umls.cui",
        "umls.protein_cui"
      ],
      "UniProtKB":[
        "uniprot.Swiss-Prot"
      ],
      "ENSEMBL":[
        "ensembl.protein"
      ]
    },
    "additional_attributes_mapping":{
      "interpro":[
        "interpro.desc"
      ]
    }
  },
  "SequenceVariant":{
    "id_ranks":[
      "CLINVAR",
      "DBSNP",
      "HGVS",
      "MYVARIANT_HG19"
    ],
    "api_name":"myvariant.info",
    "semantic":"SequenceVariant",
    "url":"https://myvariant.info/v1/query",
    "mapping":{
      "MYVARIANT_HG19":[
        "_id"
      ],
      "DBSNP":[
        "dbsnp.rsid",
        "clinvar.rsid",
        "dbnsfp.rsid"
      ],
      "HGVS":[
        "clinvar.hgvs.genomic",
        "clinvar.hgvs.protein",
        "clinvar.hgvs.coding",
        "dbnsfp.clinvar.hgvs"
      ],
      "ClINVAR":[
        "clinvar.variant_id"
      ]
    },
    "additional_attributes_mapping":{
      "cadd_consequence":[
        "cadd.consequence"
      ],
      "cadd_variant_type":[
        "cadd.type"
      ],
      "dbsnp_variant_type":[
        "dbsnp.vartype"
      ],
      "clinvar_clinical_significance":[
        "clinvar.rcv.clinical_significance"
      ],
      "sift_category":[
        "cadd.sift.cat"
      ]
    }
  },
  "SmallMolecule":{
    "id_ranks":[
      "PUBCHEM.COMPOUND",
      "CHEMBL.COMPOUND",
      "UNII",
      "CHEBI",
      "DRUGBANK",
      "MESH",
      "CAS",
      "HMDB",
      "KEGG.COMPOUND",
      "INCHI",
      "INCHIKEY",
      "UMLS",
      "LINCS",
      "name"
    ],
    "semantic":"SmallMolecule",
    "api_name":"mychem.info",
    "url":"https://mychem.info/v1/query",
    "mapping":{
      "CHEMBL.COMPOUND":[
        "chembl.molecule_chembl_id",
        "drugbank.xrefs.chembl",
        "drugcentral.xrefs.chembl_id",
        "unichem.chembl"
      ],
      "DRUGBANK":[
        "drugcentral.xrefs.drugbank_id",
        "pharmgkb.xrefs.drugbank",
        "chebi.xrefs.drugbank",
        "drugbank.id",
        "unichem.drugbank"
      ],
      "PUBCHEM.COMPOUND":[
        "pubchem.cid",
        "drugbank.xrefs.pubchem.cid",
        "drugcentral.xrefs.pubchem_cid",
        "pharmgkb.xrefs.pubchem.cid",
        "chebi.xrefs.pubchem.cid",
        "unichem.pubchem"
      ],
      "CHEBI":[
        "chebi.id",
        "chembl.chebi_par_id",
        "drugbank.xrefs.chebi",
        "drugcentral.xrefs.chebi",
        "pharmgkb.xrefs.chebi",
        "unichem.chebi"
      ],
      "UMLS":[
        "drugcentral.xrefs.umlscui",
        "pharmgkb.xrefs.umls",
        "umls.cui"
      ],
      "MESH":[
        "umls.mesh",
        "drugcentral.xrefs.mesh_descriptor_ui",
        "ginas.xrefs.MESH",
        "pharmgkb.xrefs.mesh"
      ],
      "UNII":[
        "drugcentral.xrefs.unii",
        "unii.unii",
        "aeolus.unii",
        "ginas.unii"
      ],
      "INCHIKEY":[
        "drugbank.inchi_key",
        "ginas.inchikey",
        "unii.inchikey",
        "chebi.inchikey",
        "chembl.inchi_key",
        "pubchem.inchi_key"
      ],
      "INCHI":[
        "drugbank.inchi",
        "chebi.inchi",
        "chembl.inchi",
        "pharmgkb.inchi",
        "pubchem.inchi"
      ],
      "KEGG.COMPOUND":[
        "drugbank.xrefs.kegg.cid",
        "chebi.xrefs.kegg_compound",
        "pharmgkb.xrefs.kegg_compound"
      ],
      "LINCS":[
        "unichem.lincs",
        "chebi.xrefs.lincs"
      ],
      "CAS":[
        "chebi.xrefs.cas",
        "ginas.cas_primary",
        "pharmgkb.xrefs.cas"
      ],
      "HMDB":[
        "chebi.xrefs.hmdb",
        "pharmgkb.xrefs.hmdb"
      ],
      "name":[
        "chembl.pref_name",
        "drugbank.name",
        "umls.name",
        "ginas.preferred_name",
        "pharmgkb.name",
        "chebi.name"
      ]
    },
    "additional_attributes_mapping":{
      "chembl_max_phase":[
        "chembl.max_phase"
      ],
      "chembl_molecule_type":[
        "chembl.molecule_type"
      ],
      "drugbank_drug_category":[
        "drugbank.categories.category"
      ],
      "drugbank_taxonomy_class":[
        "drugbank.taxonomy.class"
      ],
      "drugbank_groups":[
        "drugbank.groups"
      ],
      "drugbank_kingdom":[
        "drugbank.taxonomy.kingdom"
      ],
      "drugbank_superclass":[
        "drugbank.taxonomy.superclass"
      ],
      "contraindications":[
        "drugcentral.drug_use.contraindication.concept_name"
      ],
      "indications":[
        "drugcentral.drug_use.indication.concept_name"
      ],
      "mesh_pharmacology_class":[
        "drugcentral.pharmacology_class.mesh_pa.description"
      ],
      "fda_epc_pharmacology_class":[
        "drugcentral.pharmacology_class.fda_epc.description"
      ]
    }
  },
  "Drug":{
    "id_ranks":[
      "RXCUI",
      "NDC",
      "DRUGBANK",
      "PUBCHEM.COMPOUND",
      "CHEMBL.COMPOUND",
      "UNII",
      "CHEBI",
      "MESH",
      "CAS",
      "HMDB",
      "KEGG.COMPOUND",
      "INCHI",
      "INCHIKEY",
      "UMLS",
      "LINCS",
      "name"
    ],
    "semantic":"Drug",
    "api_name":"mychem.info",
    "url":"https://mychem.info/v1/query",
    "mapping":{
      "CHEMBL.COMPOUND":[
        "chembl.molecule_chembl_id",
        "drugbank.xrefs.chembl",
        "drugcentral.xrefs.chembl_id",
        "unichem.chembl"
      ],
      "DRUGBANK":[
        "drugcentral.xrefs.drugbank_id",
        "pharmgkb.xrefs.drugbank",
        "chebi.xrefs.drugbank",
        "drugbank.id",
        "unichem.drugbank"
      ],
      "PUBCHEM.COMPOUND":[
        "pubchem.cid",
        "drugbank.xrefs.pubchem.cid",
        "drugcentral.xrefs.pubchem_cid",
        "pharmgkb.xrefs.pubchem.cid",
        "chebi.xrefs.pubchem.cid",
        "unichem.pubchem"
      ],
      "CHEBI":[
        "chebi.id",
        "chembl.chebi_par_id",
        "drugbank.xrefs.chebi",
        "drugcentral.xrefs.chebi",
        "pharmgkb.xrefs.chebi",
        "unichem.chebi"
      ],
      "UMLS":[
        "drugcentral.xrefs.umlscui",
        "pharmgkb.xrefs.umls",
        "umls.cui"
      ],
      "MESH":[
        "umls.mesh",
        "drugcentral.xrefs.mesh_descriptor_ui",
        "ginas.xrefs.MESH",
        "pharmgkb.xrefs.mesh"
      ],
      "UNII":[
        "drugcentral.xrefs.unii",
        "unii.unii",
        "aeolus.unii",
        "ginas.unii"
      ],
      "INCHIKEY":[
        "drugbank.inchi_key",
        "ginas.inchikey",
        "unii.inchikey",
        "chebi.inchikey",
        "chembl.inchi_key",
        "pubchem.inchi_key"
      ],
      "INCHI":[
        "drugbank.inchi",
        "chebi.inchi",
        "chembl.inchi",
        "pharmgkb.inchi",
        "pubchem.inchi"
      ],
      "KEGG.COMPOUND":[
        "drugbank.xrefs.kegg.cid",
        "chebi.xrefs.kegg_compound",
        "pharmgkb.xrefs.kegg_compound"
      ],
      "LINCS":[
        "unichem.lincs",
        "chebi.xrefs.lincs"
      ],
      "CAS":[
        "chebi.xrefs.cas",
        "ginas.cas_primary",
        "pharmgkb.xrefs.cas"
      ],
      "HMDB":[
        "chebi.xrefs.hmdb",
        "pharmgkb.xrefs.hmdb"
      ],
      "RXCUI":[
        "ginas.xrefs.RXCUI",
        "unii.rxcui",
        "aeolus.rxcui"
      ],
      "NDC":[
        "pharmgkb.xrefs.ndc"
      ],
      "name":[
        "chembl.pref_name",
        "drugbank.name",
        "umls.name",
        "ginas.preferred_name",
        "pharmgkb.name",
        "chebi.name"
      ]
    },
    "additional_attributes_mapping":{
      "chembl_max_phase":[
        "chembl.max_phase"
      ],
      "chembl_molecule_type":[
        "chembl.molecule_type"
      ],
      "drugbank_drug_category":[
        "drugbank.categories.category"
      ],
      "drugbank_taxonomy_class":[
        "drugbank.taxonomy.class"
      ],
      "drugbank_groups":[
        "drugbank.groups"
      ],
      "drugbank_kingdom":[
        "drugbank.taxonomy.kingdom"
      ],
      "drugbank_superclass":[
        "drugbank.taxonomy.superclass"
      ],
      "contraindications":[
        "drugcentral.drug_use.contraindication.concept_name"
      ],
      "indications":[
        "drugcentral.drug_use.indication.concept_name"
      ],
      "mesh_pharmacology_class":[
        "drugcentral.pharmacology_class.mesh_pa.description"
      ],
      "fda_epc_pharmacology_class":[
        "drugcentral.pharmacology_class.fda_epc.description"
      ]
    }
  },
  "PhenotypicFeature":{
    "id_ranks":[
      "HP",
      "EFO",
      "NCIT",
      "UMLS",
      "MEDDRA",
      "MP",
      "SNOMEDCT",
      "MESH",
      "name"
    ],
    "semantic":"PhenotypicFeature",
    "api_name":"HPO API",
    "url":"https://biothings.ncats.io/hpo/query",
    "mapping":{
      "UMLS":[
        "xrefs.umls"
      ],
      "SNOMEDCT":[
        "xrefs.snomed_ct",
        "xrefs.snomedct_us"
      ],
      "HP":[
        "_id"
      ],
      "MEDDRA":[
        "xrefs.meddra"
      ],
      "EFO":[
        "xrefs.efo"
      ],
      "NCIT":[
        "xrefs.ncit"
      ],
      "MESH":[
        "xrefs.mesh"
      ],
      "MP":[
        "xrefs.mp"
      ],
      "name":[
        "name"
      ]
    }
  },
  "Disease":{
    "id_ranks":[
      "MONDO",
      "DOID",
      "OMIM",
      "ORPHANET",
      "EFO",
      "UMLS",
      "MESH",
      "MEDDRA",
      "NCIT",
      "SNOMEDCT",
      "HP",
      "GARD",
      "name"
    ],
    "semantic":"Disease",
    "api_name":"mydisease.info",
    "url":"https://mydisease.info/v1/query",
    "mapping":{
      "MONDO":[
        "mondo.mondo",
        "disgenet.xrefs.mondo"
      ],
      "DOID":[
        "mondo.xrefs.doid",
        "disease_ontology.doid",
        "disgenet.xrefs.doid"
      ],
      "UMLS":[
        "mondo.xrefs.umls",
        "mondo.xrefs.umls_cui",
        "disgenet.xrefs.umls",
        "umls.umls",
        "disease_ontology.xrefs.umls_cui"
      ],
      "name":[
        "mondo.label",
        "disgenet.xrefs.disease_name",
        "disease_ontology.name"
      ],
      "MESH":[
        "mondo.xrefs.mesh",
        "disease_ontology.xrefs.mesh",
        "ctd.mesh"
      ],
      "OMIM":[
        "mondo.xrefs.omim",
        "hpo.omim",
        "disgenet.xrefs.omim",
        "disease_ontology.xrefs.omim"
      ],
      "EFO":[
        "mondo.xrefs.efo",
        "disgenet.xrefs.efo",
        "disease_ontology.xrefs.efo"
      ],
      "ORPHANET":[
        "hpo.orphanet",
        "mondo.xrefs.orphanet"
      ],
      "GARD":[
        "mondo.xrefs.gard",
        "disease_ontology.xrefs.gard"
      ],
      "HP":[
        "mondo.xrefs.hp",
        "disgenet.xrefs.hp"
      ],
      "SNOMEDCT":[
        "mondo.xrefs.sctid",
        "umls.snomed.preferred",
        "umls.snomed.non-preferred"
      ],
      "NCIT":[
        "mondo.xrefs.ncit",
        "disease_ontology.xrefs.ncit"
      ],
      "MEDDRA":[
        "mondo.xrefs.meddra",
        "disease_ontology.xrefs.meddra"
      ]
    }
  },
  "ClinicalFinding":{
    "id_ranks":[
      "LOINC",
      "NCIT",
      "EFO",
      "name"
    ],
    "semantic":"Disease",
    "api_name":"mydisease.info",
    "url":"https://mydisease.info/v1/query",
    "mapping":{
      "LOINC":[
        "mondo.xrefs.loinc"
      ],
      "NCIT":[
        "mondo.xrefs.ncit",
        "disease_ontology.xrefs.ncit"
      ],
      "EFO":[
        "mondo.xrefs.efo",
        "disgenet.xrefs.efo",
        "disease_ontology.xrefs.efo"
      ],
      "name":[
        "mondo.label",
        "disgenet.xrefs.disease_name",
        "disease_ontology.name"
      ]
    }
  },
  "MolecularActivity":{
    "id_ranks":[
      "GO",
      "REACT",
      "RHEA",
      "MetaCyc",
      "KEGG.REACTION",
      "name"
    ],
    "semantic":"MolecularActivity",
    "api_name":"Gene Ontology Molecular Function API",
    "url":"https://biothings.ncats.io/go_mf/query",
    "mapping":{
      "GO":[
        "_id"
      ],
      "MetaCyc":[
        "xrefs.metacyc"
      ],
      "RHEA":[
        "xrefs.rhea"
      ],
      "KEGG.REACTION":[
        "xrefs.kegg_reaction"
      ],
      "REACT":[
        "xrefs.reactome"
      ],
      "name":[
        "name"
      ]
    }
  },
  "BiologicalProcess":{
    "id_ranks":[
      "GO",
      "REACT",
      "MetaCyc",
      "KEGG",
      "name"
    ],
    "semantic":"BiologicalProcess",
    "api_name":"Gene Ontology Biological Process API",
    "url":"https://biothings.ncats.io/go_bp/query",
    "mapping":{
      "GO":[
        "_id"
      ],
      "MetaCyc":[
        "xrefs.metacyc"
      ],
      "KEGG":[
        "xrefs.kegg_pathway"
      ],
      "REACT":[
        "xrefs.reactome"
      ],
      "name":[
        "name"
      ]
    }
  },
  "CellularComponent":{
    "id_ranks":[
      "GO",
      "MetaCyc",
      "name"
    ],
    "semantic":"CellularComponent",
    "api_name":"Gene Ontology Cellular Component API",
    "url":"https://biothings.ncats.io/go_cc/query",
    "mapping":{
      "GO":[
        "_id"
      ],
      "MetaCyc":[
        "xrefs.metacyc"
      ],
      "name":[
        "name"
      ]
    }
  },
  "Pathway":{
    "id_ranks":[
      "GO",
      "REACT",
      "KEGG",
      "SMPDB",
      "PHARMGKB.PATHWAYS",
      "WIKIPATHWAYS",
      "BIOCARTA",
      "name"
    ],
    "semantic":"Pathway",
    "api_name":"Geneset API",
    "url":"https://biothings.ncats.io/geneset/query",
    "mapping":{
      "REACT":[
        "reactome"
      ],
      "WIKIPATHWAYS":[
        "wikipathways"
      ],
      "KEGG":[
        "kegg"
      ],
      "BIOCARTA":[
        "biocarta"
      ],
      "PHARMGKB.PATHWAYS":[
        "pharmgkb"
      ],
      "GO":[
        "go"
      ],
      "SMPDB":[
        "smpdb"
      ],
      "name":[
        "name"
      ]
    },
    "additional_attributes_mapping":{
      "num_of_participants":[
        "num_of_participants"
      ]
    }
  },
  "AnatomicalEntity":{
    "id_ranks":[
      "UBERON",
      "UMLS",
      "MESH",
      "NCIT",
      "name"
    ],
    "semantic":"AnatomicalEntity",
    "api_name":"UBERON API",
    "url":"https://biothings.ncats.io/uberon/query",
    "mapping":{
      "UBERON":[
        "_id"
      ],
      "UMLS":[
        "xrefs.umls"
      ],
      "MESH":[
        "xrefs.mesh"
      ],
      "NCIT":[
        "xrefs.ncit"
      ],
      "name":[
        "name"
      ]
    }
  },
  "Cell":{
    "id_ranks":[
      "CL",
      "NCIT",
      "MESH",
      "EFO",
      "name"
    ],
    "semantic":"Cell",
    "api_name":"Cell Ontology API",
    "url":"https://biothings.ncats.io/cell_ontology/query",
    "mapping":{
      "CL":[
        "_id"
      ],
      "NCIT":[
        "xrefs.ncit"
      ],
      "MESH":[
        "xrefs.mesh"
      ],
      "EFO":[
        "xrefs.efo"
      ],
      "name":[
        "name"
      ]
    }
  }
}