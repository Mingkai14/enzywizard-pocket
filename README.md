[![DOI](https://zenodo.org/badge/1219037424.svg)](https://doi.org/10.5281/zenodo.19709998)
# EnzyWizard-Pocket

EnzyWizard-Pocket is a command-line tool for detecting and characterizing
binding pockets from a cleaned protein structure and generating a detailed JSON report.
It takes a cleaned CIF or PDB file as input and identifies binding pockets using 
PyVOL, a geometry-based pocket detection program. PyVOL detects binding pockets by 
simulating probe spheres rolling over the protein surface,
identifying cavities based on geometric accessibility and spatial continuity.
Each detected binding pocket is represented as a cluster of spheres and characterized
by its volume, box size, and associated residues.
The tool outputs structured binding pocket information suitable for downstream applications
such as docking, binding site analysis, and enzyme characterization.


# Documentation index:

- example usage
- input parameters
- output files
- output report schema
- Process
- common errors and solutions
- dependencies
- references


# example usage:

The examples below use placeholder paths such as `path/to/input.cif` and
`path/to/output_dir/`; replace them with your own cleaned input structure file
and output directory.

Detect binding pockets from a cleaned CIF file with default settings. The default
PyVOL probe radius range is 1.8 to 6.2, and the default minimum pocket volume is
50 cubic angstroms.

```
enzywizard-pocket -i path/to/input.cif -o path/to/output_dir/
```

Detect binding pockets from a cleaned PDB file with default settings.

```
enzywizard-pocket -i path/to/input.pdb -o path/to/output_dir/
```

Detect binding pockets using long option names.

```
enzywizard-pocket --input_path path/to/input.cif --output_dir path/to/output_dir/
```

Use a smaller minimum probe radius to make PyVOL more sensitive to narrow or
fine-grained cavities. Excessively small values can make PyVOL fail, so this is
best used when narrow pockets are expected and the default settings miss them.

```
enzywizard-pocket -i path/to/input.cif -o path/to/output_min_rad_1_4/ --min_rad 1.4
```

Use a larger minimum probe radius to ignore very narrow cavities and focus on
larger accessible pocket regions. This can reduce small-pocket detections, but
may miss narrow binding sites.

```
enzywizard-pocket -i path/to/input.cif -o path/to/output_min_rad_2_2/ --min_rad 2.2
```

Use a larger maximum probe radius to allow broader pocket expansion and more
exposed cavity detection. Excessively large values can make PyVOL fail and may
increase runtime.

```
enzywizard-pocket -i path/to/input.cif -o path/to/output_max_rad_8_0/ --max_rad 8.0
```

Use a smaller minimum volume threshold to retain smaller predicted pockets. This
can increase the number of reported pockets and may include less relevant small
cavities.

```
enzywizard-pocket -i path/to/input.cif -o path/to/output_min_volume_25/ --min_volume 25
```

Use a larger minimum volume threshold to report only larger binding pockets.
This filters out smaller pockets and can make the report shorter.

```
enzywizard-pocket -i path/to/input.cif -o path/to/output_min_volume_200/ --min_volume 200
```

Combine probe-radius and volume settings when screening for broad, high-volume
pockets. Comparing this report with the default report is useful for checking how
sensitive pocket detection is to PyVOL parameters.

```
enzywizard-pocket -i path/to/input.cif -o path/to/output_broad_pockets/ --min_rad 2.0 --max_rad 8.0 --min_volume 200
```



# input parameters:

-i, --input_path
Required.
Path to the input cleaned protein structure file.
Supported file extensions: .cif, .pdb.

-o, --output_dir
Required.
Path to the output directory for saving the JSON report.
The output directory is created automatically if it does not exist.

--min_rad
Optional.
Minimum probe radius used in PyVOL cavity detection.
This parameter controls the smallest probe sphere used to explore cavities.
Default: 1.8.
Must be greater than or equal to 1.2 and must be smaller than --max_rad.
Smaller values allow detection of narrow and fine-grained binding pockets, but
excessively small values may lead to PyVOL failure. Larger values ignore very
narrow cavities and focus on larger accessible pocket regions, but may miss
narrow binding sites.

--max_rad
Optional.
Maximum probe radius used in PyVOL cavity detection.
This parameter controls the largest probe sphere used during cavity expansion.
Default: 6.2.
Must be greater than --min_rad.
Larger values allow identification of broader and more exposed binding pockets,
but excessively large values may lead to PyVOL failure and may increase runtime.
Smaller values limit pocket expansion and may miss broader cavities.

--min_volume
Optional.
Minimum binding pocket volume threshold.
Default: 50.
Must be greater than 20.
Only binding pockets with volume greater than or equal to this value will be
retained. Smaller values retain more small predicted pockets and may include
less relevant cavities. Larger values filter out smaller pockets and produce a
shorter report focused on larger pocket regions.


# output files:

The program outputs the following files into the output directory:

`{name}` is derived from the input file name without its extension.

1. A JSON report
   - pocket_report_{name}.json
     - JSON report containing binding pocket statistics and binding pocket details.

2. A log file
   - log.txt
     - Processing log containing informational messages and errors.


# output report schema:

The JSON report contains the following fields:

   - "report_type"
     - Data type: string
     - Expected value: "enzywizard_pocket"
     - Description: The field "report_type" indicates the type of report ("report": http://purl.obolibrary.org/obo/IAO_0000088) generated by the EnzyWizard-Pocket software.

   - "binding_pocket_statistics"
     - Data type: object
     - Description: The field "binding_pocket_statistics" indicates the summary statistics ("statistics": http://purl.obolibrary.org/obo/STATO_0000039) of binding pockets ("binding pocket": https://schlessinger-lab.github.io/pyvol/index.html) calculated from the protein structure ("protein structure": http://edamontology.org/data_1537) by PyVOL software ("PyVOL": https://bio.tools/PyVOL).

     The "binding_pocket_statistics" object contains:

     - "binding_pocket_count"
       - Data type: integer
       - Description: The field "binding_pocket_count" indicates the count of binding pockets ("binding pocket": https://schlessinger-lab.github.io/pyvol/pocket_specification.html) calculated by PyVOL software ("PyVOL": https://bio.tools/PyVOL).

     - "max_binding_pocket_volume"
       - Data type: number
       - Description: The field "max_binding_pocket_volume" indicates the maximum volume ("volume": http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ("binding pocket": https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ("PyVOL": https://bio.tools/PyVOL). Unit: cubic angstroms (Å^3) ("cubic angstrom": http://qudt.org/vocab/unit/ANGSTROM3).

     - "total_binding_pocket_volume"
       - Data type: number
       - Description: The field "total_binding_pocket_volume" indicates the total volume ("volume": http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ("binding pocket": https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ("PyVOL": https://bio.tools/PyVOL). Unit: cubic angstroms (Å^3) ("cubic angstrom": http://qudt.org/vocab/unit/ANGSTROM3).

   - "binding_pockets"
     - Data type: array
     - Description: The field "binding_pockets" indicates binding pockets ("binding pocket": https://schlessinger-lab.github.io/pyvol/index.html) in the protein structure ("protein structure": http://edamontology.org/data_1537) calculated by PyVOL software ("PyVOL": https://bio.tools/PyVOL).

     Each item in "binding_pockets" is an object containing:

     - "binding_pocket_volume"
       - Data type: number
       - Description: The field "binding_pocket_volume" indicates the volume ("volume": http://purl.obolibrary.org/obo/PATO_0000918) of a binding pocket ("binding pocket": https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ("PyVOL": https://bio.tools/PyVOL). Unit: cubic angstroms (Å^3) ("cubic angstrom": http://qudt.org/vocab/unit/ANGSTROM3).

     - "binding_pocket_sphere_count"
       - Data type: integer
       - Description: The field "binding_pocket_sphere_count" indicates the count of spheres ("sphere": https://mathworld.wolfram.com/Sphere.html) used to represent a binding pocket ("binding pocket": https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ("PyVOL": https://bio.tools/PyVOL).

     - "residues"
       - Data type: array
       - Description: The field "residues" indicates the residues ("residue": https://schlessinger-lab.github.io/pyvol/index.html).

       Each item in "residues" is an object containing:

       - "residue_index"
         - Data type: integer
         - Description: The field "residue_index" indicates the index ("index": http://purl.obolibrary.org/obo/NCIT_C25390) of the residue ("residue": http://purl.obolibrary.org/obo/GENO_0000782).

       - "residue_name"
         - Data type: string
         - Allowed values: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y.
         - Description: The field "residue_name" indicates the name of the residue ("residue": http://purl.obolibrary.org/obo/GENO_0000782), using one-letter code ("one-letter code": https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent.

     - "binding_pocket_center_coordinate"
       - Data type: array
       - Length: 3
       - Item data type: number
       - Description: The field "binding_pocket_center_coordinate" indicates the center coordinate ("coordinate": https://mathworld.wolfram.com/Coordinates.html) of a binding pocket ("binding pocket": https://schlessinger-lab.github.io/pyvol/index.html) in the protein structure ("protein structure": http://edamontology.org/data_1537). Unit: angstroms (Å) ("angstrom": http://qudt.org/vocab/unit/ANGSTROM).

     - "binding_pocket_box_size"
       - Data type: array
       - Length: 3
       - Item data type: number
       - Description: The field "binding_pocket_box_size" indicates the size ("size": http://purl.obolibrary.org/obo/PATO_0000117) of the box ("box": https://www.pbr-book.org/3ed-2018/Geometry_and_Transformations/Bounding_Boxes) enclosing a binding pocket ("binding pocket": https://schlessinger-lab.github.io/pyvol/index.html) in the protein structure ("protein structure": http://edamontology.org/data_1537). Unit: angstroms (Å) ("angstrom": http://qudt.org/vocab/unit/ANGSTROM).


# Process:

This command processes the input cleaned protein structure as follows:

1. Load the input structure
   - Read the cleaned CIF or PDB file using Biopython (Bio.PDB).
   - Resolve the protein name from the input filename.

2. Validate input conditions
   - Check that the input file exists.
   - Validate that the structure satisfies the cleaned-structure requirement.

3. Extract structural information
   - Retrieve the single protein chain.
   - Extract residue list and establish residue identity mapping.

4. Prepare PyVOL input
   - Convert the structure into temporary PDB file.
   - Generate a temporary PyVOL configuration file specifying probe radii and volume threshold.

5. Run PyVOL for binding pocket detection
   - Execute PyVOL using a rolling probe sphere algorithm.
   - Probe spheres with radii ranging from min_rad to max_rad explore the protein surface.
   - Cavities are identified based on geometric accessibility and spatial continuity.
   - Binding pockets are represented as clusters of overlapping spheres.

6. Parse PyVOL outputs
   - Read sphere coordinates and radii from .xyzrg files in temporary directory.
   - Extract binding pocket volumes from .rept report files in temporary directory.
   - Identify valid binding pocket object pairs (.obj and .xyzrg).

7. Compute binding pocket features
   - Calculate binding pocket center coordinates using bounding box of spheres.
   - Compute binding pocket box size.
   - Map binding pocket spheres to nearest residues based on spatial proximity.

8. Filter binding pockets
   - Remove binding pockets with missing volume or invalid geometry.
   - Remove binding pockets lacking valid residue associations.

9. Sort binding pockets
   - Sort valid binding pockets by volume in descending order.

10. Compute summary statistics
   - Calculate total number of binding pockets.
   - Determine maximum and total binding pocket volumes.

11. Save outputs
   - Generate and save a JSON report containing binding pockets and summary statistics.


# common errors and solutions:

- "Invalid pocket parameters"
  - Cause: One or more PyVOL parameters are outside the supported range. `--min_rad` must be at least 1.2, `--max_rad` must be greater than `--min_rad`, and `--min_volume` must be greater than 20.
  - Solution: Use standard values such as `--min_rad 1.8 --max_rad 6.2 --min_volume 50`, then adjust one parameter at a time if needed.

- "Input not found"
  - Cause: The path passed to `-i` or `--input_path` does not exist or is not a file.
  - Solution: Check the input file path and make sure it points to an existing cleaned CIF or PDB file.

- "Filename too long"
  - Cause: The input file name without extension is longer than the supported filename limit.
  - Solution: Rename the input file to a shorter name and run the command again.

- "Unsupported format"
  - Cause: The input file extension is not `.cif` or `.pdb`.
  - Solution: Use a supported cleaned structure file format.

- "Exception in loading structure for"
  - Cause: Biopython could not parse the input file as a usable structure.
  - Solution: Check that the file is valid, non-empty, non-corrupted, and matches its file extension.

- "Structure must contain exactly one model. Please run 'enzywizard clean' first."
  - Cause: The input structure contains zero models or multiple models.
  - Solution: Run the structure through `enzywizard-clean` first and use the cleaned output as input.

- "Structure must contain exactly one chain. Please run 'enzywizard clean' first."
  - Cause: The input structure contains zero chains or multiple chains.
  - Solution: Run the structure through `enzywizard-clean` first so the input has a single cleaned chain.

- "Cleaned structure must use chain ID 'A'. Please run 'enzywizard clean' first."
  - Cause: The input structure is not in the cleaned single-chain format expected by EnzyWizard-Pocket.
  - Solution: Use the cleaned output generated by `enzywizard-clean`.

- "Non-protein or hetero residue detected"
  - Cause: The input still contains heterogens, water, ligands, or other non-protein residues.
  - Solution: Run `enzywizard-clean` first and use the cleaned CIF or PDB output.

- "Insertion code detected"
  - Cause: The input contains insertion codes and is not in the expected continuous cleaned residue numbering.
  - Solution: Run `enzywizard-clean` first and use the cleaned output.

- "Residue numbering is not continuous"
  - Cause: Residue indices do not start at 1 and continue without gaps.
  - Solution: Run `enzywizard-clean` first to renumber the structure.

- "Missing backbone atom"
  - Cause: A residue is missing a required backbone atom.
  - Solution: Run `enzywizard-clean` first. If the error remains, check the input structure quality.

- "Missing heavy atoms" or "Unexpected heavy atoms"
  - Cause: A residue is missing required heavy atoms, or contains heavy atoms that are not expected for its standardized residue type.
  - Solution: Run `enzywizard-clean` first and inspect the affected residue reported in `log.txt` if the error remains.

- "Failed to run PyVOL"
  - Cause: The PyVOL executable could not be started, usually because PyVOL is not installed or is not available on `PATH`.
  - Solution: Install PyVOL and confirm that the `pyvol` command can be run from the same environment.

- "PyVOL failed with return code"
  - Cause: PyVOL started but returned an error. Common causes include unsuitable probe-radius settings, problematic cleaned input geometry, or a PyVOL environment issue.
  - Solution: Review the PyVOL output tail in `log.txt`, try default parameters, and then adjust `--min_rad`, `--max_rad`, or `--min_volume` gradually.

- "No pockets detected by PyVOL"
  - Cause: PyVOL completed but did not detect any pocket files for the selected structure and parameters.
  - Solution: This can be a valid result. If pockets are expected, try a smaller `--min_volume`, a smaller `--min_rad`, or a larger `--max_rad`.

- "PyVOL output incomplete"
  - Cause: PyVOL finished without the output files needed for pocket parsing.
  - Solution: Review `log.txt`, confirm PyVOL is working in the environment, and rerun with standard parameters.

- "No valid pocket obj/xyzrg pairs found"
  - Cause: PyVOL output files were present but could not be matched into complete pocket object and sphere-file pairs.
  - Solution: Review the PyVOL output in `log.txt` and rerun with default pocket parameters.

- "No PyVOL report (.rept) files found"
  - Cause: PyVOL did not produce a report file containing pocket volumes.
  - Solution: Check the PyVOL run details in `log.txt` and confirm the PyVOL installation is functioning.

- "No valid spheres found in xyzrg file"
  - Cause: A PyVOL sphere file was empty or did not contain parseable sphere coordinates and radii.
  - Solution: Rerun with standard parameters and check whether PyVOL produced valid `.xyzrg` output.

- "No valid pockets found after filtering"
  - Cause: Candidate pockets were detected, but all were removed because they lacked volume, valid geometry, or residue associations.
  - Solution: Try a smaller `--min_volume` or less restrictive probe-radius settings, and check that the cleaned input structure is valid.

- "Failed to write report JSON to"
  - Cause: The report could not be written to the output directory because of a filesystem, permission, or path problem.
  - Solution: Check that the `-o` output directory path is writable and that there is enough disk space.

- Cleaned structure validation failed
  - Cause: The input is not a valid EnzyWizard-cleaned single-chain protein structure. Common causes include multiple chains, non-chain-A input, heterogens, insertion codes, non-standard residues, missing atoms, unexpected atoms, invalid occupancies, or non-continuous numbering.
  - Solution: Review the specific validation error above this summary in `log.txt`, run `enzywizard-clean`, and use its cleaned CIF or PDB output.

- Pocket regions calculation failed
  - Cause: Structure extraction, PyVOL execution, PyVOL output parsing, or pocket filtering failed.
  - Solution: Review the specific error above this summary in `log.txt`, then check the cleaned input structure, PyVOL installation, and pocket parameter values.

- Failed to generate pocket report
  - Cause: The detected pocket data could not be converted into the report structure.
  - Solution: Review earlier pocket calculation errors in `log.txt` and rerun after fixing the upstream problem.

- Output files are missing
  - Cause: The command failed before all outputs were written, or the output directory is not the directory passed to `-o`.
  - Solution: Check `log.txt`, confirm the `-o` output directory, and rerun after fixing earlier errors.

- Output file names are different from expected
  - Cause: Output names use `{name}`, which is derived from the input file name without its extension.
  - Solution: Check the input file name and look for `pocket_report_{name}.json` and `log.txt` in the output directory.


# dependencies:

- Biopython
- PyVOL
- NumPy


# references:

- Guerra JV, et al. PyVOL: a PyMOL plugin for visualization, comparison,
  and volume calculation of drug-binding sites. Bioinformatics. 2021.

- PyVOL:
  https://github.com/schlessinger-lab/pyvol

- Biopython:
  https://biopython.org/
