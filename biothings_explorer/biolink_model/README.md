# BioLink Model

A python library for manipulating BioLink Model.

## 📐 Usage

### 📢 Import and Initialize

```python
from biothings_explorer.biolink_model.biolink import BioLink
biolink = BioLink()
```

### ❗ Load BioLink Yaml File

Loading BioLink Yaml file is a required step before you can utilizing this package to traverse the hierarchy tree for BioLink predicates and classes.

The Yaml file can be loaded through a url, a local file stored within the package, or a valid file path provided.

#### 🔎 Load the BioLink-model yaml file stored along with the package

This can be done in sync or async mode.

```python
# load in async mode
biolink.load()
# in sync mode
biolink.load_sync()
```

#### 🔎 Load the BioLink-model yaml file from a valid url

```python
# load in async mode
# the url provided below points to the most recent version of the biolink model.
biolink.load("https://raw.githubusercontent.com/biolink/biolink-model/master/biolink-model.yaml")
```

#### 🔎 Load the BioLink-model yaml file from a local file path

This can be done in sync or async mode as well.

```python
import os
# load in async mode
# assume your biolink file is stored in the same folder under biolink.yaml
file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))

biolink.load(file_path)
# in sync mode
biolink.load_sync(file_path)
```

### ❇️ Traverse the BioLink Class Hierarchy

#### 🔎 Get BioLink Class Tree Object

```python
tree = biolink.class_tree
```

#### 🔎 Get the ancestors of a biolink class

```python
tree = biolink.class_tree

ancestors = tree.get_ancestors("Gene")
```

#### 🔎 Get the descendants of a biolink class

```python
tree = biolink.class_tree

descendants = tree.get_descendants("MolecularEntity")
```

### ❇️ Traverse the BioLink Slot Hierarchy

#### 🔎 Get BioLink Slot Tree Object

```python
tree = biolink.slot_tree
```

#### 🔎 Get the ancestors of a biolink slot

```python
tree = biolink.slot_tree

ancestors = tree.get_ancestors("regulates")
```