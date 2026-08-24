---
search:
  boost: 2.0
---


# Enum: LicenseEnum 




_model/shared.model.csv's license Valid Values list Apache_2.0/GPL_3.0; the standalone CV reference model/valid_values.csv instead documents Apache_2/GPL_3 (no ".0"/"3.0" suffix) for the same two licenses. This enum keeps shared.model.csv's spelling (the attribute's actual schematic Valid Values) and carries the valid_values.csv description over unchanged — the naming mismatch between the two source CSVs is a real data-quality finding, not resolved here._



<div data-search-exclude markdown="1">

URI: [governanceduo:enum/LicenseEnum](https://w3id.org/sage-bionetworks/governance-duo/enum/LicenseEnum)

## Permissible Values
| Value | Meaning | Description |
| --- | --- | --- |
| CC0 | None | Creative Commons Zero license, allowing for the free use of the data |
| CC_BY | None | Creative Commons Attribution license, requiring attribution to the original s... |
| CC_BY_NC | None | Creative Commons Attribution-NonCommercial license, allowing for non-commerci... |
| CC_BY_ND | None | Creative Commons Attribution-NoDerivatives license, allowing for redistributi... |
| CC_BY_SA | None | Creative Commons Attribution-ShareAlike license, allowing for modifications w... |
| CC_BY_NC_ND | None | Creative Commons Attribution-NonCommercial-NoDerivatives license, allowing fo... |
| CC_BY_NC_SA | None | Creative Commons Attribution-NonCommercial-ShareAlike license, allowing for n... |
| Apache_2.0 | None | Apache License 2 |
| MIT | None | MIT License, a permissive license allowing for use, modification, and distrib... |
| GPL_3.0 | None | GNU General Public License v3 |
| BSD_3_Clause | None | BSD 3-Clause License, a permissive license allowing for use, modification, an... |




## Slots

| Name | Description |
| ---  | --- |
| [license](../slots/license.md) | The license under which the data associated with the access requirement is sh... |










## Identifier and Mapping Information





### Schema Source


* from schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo






## LinkML Source

<details>
```yaml
name: LicenseEnum
description: model/shared.model.csv's license Valid Values list Apache_2.0/GPL_3.0;
  the standalone CV reference model/valid_values.csv instead documents Apache_2/GPL_3
  (no ".0"/"3.0" suffix) for the same two licenses. This enum keeps shared.model.csv's
  spelling (the attribute's actual schematic Valid Values) and carries the valid_values.csv
  description over unchanged — the naming mismatch between the two source CSVs is
  a real data-quality finding, not resolved here.
from_schema: https://w3id.org/sage-bionetworks/governance-duo/governance_duo
rank: 1000
permissible_values:
  CC0:
    text: CC0
    description: Creative Commons Zero license, allowing for the free use of the data.
  CC_BY:
    text: CC_BY
    description: Creative Commons Attribution license, requiring attribution to the
      original source.
  CC_BY_NC:
    text: CC_BY_NC
    description: Creative Commons Attribution-NonCommercial license, allowing for
      non-commercial use with attribution.
  CC_BY_ND:
    text: CC_BY_ND
    description: Creative Commons Attribution-NoDerivatives license, allowing for
      redistribution with attribution but no modifications.
  CC_BY_SA:
    text: CC_BY_SA
    description: Creative Commons Attribution-ShareAlike license, allowing for modifications
      with attribution and sharing under the same license.
  CC_BY_NC_ND:
    text: CC_BY_NC_ND
    description: Creative Commons Attribution-NonCommercial-NoDerivatives license,
      allowing for non-commercial use with attribution but no modifications.
  CC_BY_NC_SA:
    text: CC_BY_NC_SA
    description: Creative Commons Attribution-NonCommercial-ShareAlike license, allowing
      for non-commercial modifications with attribution and sharing under the same
      license.
  Apache_2.0:
    text: Apache_2.0
    description: Apache License 2.0, a permissive license allowing for use, modification,
      and distribution.
  MIT:
    text: MIT
    description: MIT License, a permissive license allowing for use, modification,
      and distribution.
  GPL_3.0:
    text: GPL_3.0
    description: GNU General Public License v3.0, a copyleft license requiring derivative
      works to be licensed under the same terms.
  BSD_3_Clause:
    text: BSD_3_Clause
    description: BSD 3-Clause License, a permissive license allowing for use, modification,
      and distribution with attribution.

```
</details>

</div>