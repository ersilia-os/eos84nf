# GenMol Superstructure Generation

Grows an input molecule into up to 100 larger drug-like molecules, each containing the whole input. GenMol, from NVIDIA, applies masked discrete diffusion over the SAFE fragment representation, revealing fragment blocks in parallel rather than emitting a string token by token, which beats the earlier autoregressive SAFE-GPT on validity, molecular quality and diversity while sampling faster. Training used the SAFE corpus built from ZINC and UniChem. Sampling is stochastic and unseeded, and duplicates or copies of the input are discarded, so fewer than 100 molecules often come back.

This model was incorporated on 2026-08-04.Last packaged on 2026-10-26.

## Information
### Identifiers
- **Ersilia Identifier:** `eos84nf`
- **Slug:** `genmol-superstructure`

### Domain
- **Task:** `Sampling`
- **Subtask:** `Generation`
- **Biomedical Area:** `Any`
- **Target Organism:** `Any`
- **Tags:** `Compound generation`, `Chemical language model`, `ZINC`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `100`
- **Output Consistency:** `Variable`
- **Interpretation:** Up to 100 larger molecules that contain the whole input, extended with new fragments; unseeded so runs differ.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| smi_00 | string |  | Generated compound index 0 extending the input molecule with new fragments using GenMol |
| smi_01 | string |  | Generated compound index 1 extending the input molecule with new fragments using GenMol |
| smi_02 | string |  | Generated compound index 2 extending the input molecule with new fragments using GenMol |
| smi_03 | string |  | Generated compound index 3 extending the input molecule with new fragments using GenMol |
| smi_04 | string |  | Generated compound index 4 extending the input molecule with new fragments using GenMol |
| smi_05 | string |  | Generated compound index 5 extending the input molecule with new fragments using GenMol |
| smi_06 | string |  | Generated compound index 6 extending the input molecule with new fragments using GenMol |
| smi_07 | string |  | Generated compound index 7 extending the input molecule with new fragments using GenMol |
| smi_08 | string |  | Generated compound index 8 extending the input molecule with new fragments using GenMol |
| smi_09 | string |  | Generated compound index 9 extending the input molecule with new fragments using GenMol |

_10 of 100 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos84nf](https://hub.docker.com/r/ersiliaos/eos84nf)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos84nf.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos84nf.zip)

### Resource Consumption
- **Model Size (Mb):** `1334`
- **Environment Size (Mb):** `2239`
- **Image Size (Mb):** `4849.38`

**Computational Performance (seconds):**
- 10 inputs: `407.77`
- 100 inputs: `-1`
- 10000 inputs: `-1`

### References
- **Source Code**: [https://github.com/NVIDIA-Digital-Bio/genmol](https://github.com/NVIDIA-Digital-Bio/genmol)
- **Publication**: [https://doi.org/10.48550/arXiv.2501.06158](https://doi.org/10.48550/arXiv.2501.06158)
- **Publication Type:** `Preprint`
- **Publication Year:** `2025`
- **Ersilia Contributor:** [arnaucoma24](https://github.com/arnaucoma24)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [Apache-2.0](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos84nf
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos84nf
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
