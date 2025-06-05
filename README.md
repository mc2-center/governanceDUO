
The Data Use Ontology (DUO) provides a helpful framework for gating access to data managed by Sage Bionetworks on the Synapse platform. 

[DUO was developed by members of the Global Alliance for Genomic Health (GA4GH)](https://github.com/EBISPOT/DUO/blob/master/README.md): "DUO allows [users] to semantically tag datasets with restriction about their usage, making them discoverable automatically based on the authorization level of users, or intended usage".

At Sage, we extended DUO modifiers for our use cases and incorporated [derived annotations](https://sagebionetworks.jira.com/wiki/spaces/PLFM/pages/2597617665/API+Changes+to+support+Extension+of+Data+Access+Management+to+Users+outside+of+Sage+ACT) as a way of scaling governance support on projects by assigning access requirements (ARs)* to entities based on its DUO annotation.

_*ARs are applied in the form of a clickwrap (i.e., the user must agree to terms) and/or a managed access requirement (i.e., the user must provide evidence). Managed ARs may require evidence in the form of **Authentication** (e.g., training certification, profile validation, two-factor authorization) and/or **Authorization** (e.g., intended data use (IDU) statement, data use certificate (DUC), ethics approval letter from an institutional review board (IRB) or independent ethics committee (IEC))._


# Resources
 - [GA4GH Products](https://www.ga4gh.org/product/data-use-ontology-duo/)
 - [EBISPOT DUO](https://github.com/EBISPOT/DUO/blob/master/README.md)
 - [Extension of Data Access Management](https://sagebionetworks.jira.com/wiki/spaces/PLFM/pages/2597617665/API+Changes+to+support+Extension+of+Data+Access+Management+to+Users+outside+of+Sage+ACT)


# Related Publications
 - The Data Use Ontology to streamline responsible access to human biomedical datasets. Lawson, Jonathan et al., Cell Genomics, Volume 1, Issue 2, 100028, doi: https://doi.org/10.1016/j.xgen.2021.100028
 - Aligning NIH’s existing data use restrictions to the GA4GH DUO standard. Lawson, Jonathan et al., Cell Genomics, Volume 3, Issue 9, 100381, doi: https://doi.org/10.1016/j.xgen.2023.100381
 - Enhancing Data Use Ontology (DUO) for health-data sharing by extending it with ODRL and DPV. Pandit HJ, Esteves B., Semantic Web. 2024;15(4):1473-1498, doi: https://doi.org/10.3233/SW-243583
 - Getting your DUCs in a row - standardising the representation of Digital Use Conditions. Jeanson, F., Gibson, S.J., Alper, P. et al., Sci Data 11, 464 (2024), doi: https://doi.org/10.1038/s41597-024-03280-6
