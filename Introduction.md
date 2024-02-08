The Data Use Ontology (DUO) provides a helpful framework for gating access to data managed by Sage Bionetworks on the Synapse platform. 

[DUO was developed by members of the Global Alliance for Genomic Health (GA4GH)](https://github.com/EBISPOT/DUO/blob/master/README.md): "DUO allows [users] to semantically tag datasets with restriction about their usage, making them discoverable automatically based on the authorization level of users, or intended usage".

At Sage, we extended DUO modifiers for our use cases (see figure below) and incorporated [derived annotations](https://sagebionetworks.jira.com/wiki/spaces/PLFM/pages/2597617665/API+Changes+to+support+Extension+of+Data+Access+Management+to+Users+outside+of+Sage+ACT) as a way of scaling governance support on projects by assigning access requirements (ARs)* to entities based on its DUO annotation.

_*ARs are applied in the form of a clickwrap (i.e., user must agree to terms) and/or a managed access requirement (i.e., user must provide evidence). Managed ARs may require evidence in the form of **Authentication** (e.g., training certification, profile validation, two-factor authorization) and/or **Authorization** (e.g., intended data use (IDU) statement, data use certificate (DUC), ethics approval letter from an institutional review board (IRB) or independent ethics committee (IEC))._


# Resources
 - [EBISPOT DUO](https://github.com/EBISPOT/DUO/blob/master/README.md)
 - [Extension of Data Access Management](https://sagebionetworks.jira.com/wiki/spaces/PLFM/pages/2597617665/API+Changes+to+support+Extension+of+Data+Access+Management+to+Users+outside+of+Sage+ACT)


# Publications
 - https://doi.org/10.1016/j.xgen.2023.100381
 - https://www.semantic-web-journal.net/system/files/swj3583.pdf
