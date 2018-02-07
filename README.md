# Hydra  
![Logo](https://github.com/joshua-barber/hydra/blob/master/hydra.png)    
Multi-headed connector for rapid data extraction from new environments.

# Description
Hydra is a rapid extraction tool for use in novel data infrastructure environments.
    Its purpose is to provide a wide selection of simple data source handlers which can be manipulated and combined to create
    multi-headed one-shot data extractions for processing in a more powerful cloud environment.  
    Given only environment credentials, Hydra will assist with:  
        + Enumerating all data elements for target servers  
        + Providing summary statistics for later reconciliation  
        + Investigating specific elements   
        + Marking elements for extraction  
        + Efficient bulk transfer to a cloud or local storage solution  
        + Post-transfer reconciliation  

    Hydra's purpose is NOT to be a set-and-forget data pipeline as this is better suited to existing pipeline tools such as Spotify's Luigi.
    Instead Hydra should be used to build a solid POC from which a better optimised and tailored pipeline can be built. It balances between
    full-featured libraries for single data sources (i.e. TableauServerClient, AWS CLI), and simple data extractors which limit access 
    to the underlying datasource (i.e. Pandas' IO Tools). This minimises the upfront investment required to develop an inital analytics 
    solution while also avoiding the need for an expensive re-build as the project matures. Simply fork the Hydra repository and expand its 
    pre-built connectors to suit your tailored pipeline. Hydra's handlers are simple to modify by design and will make use of the most 
    extensible data connector available for any given target data source. 

    There are two modules implemented by Hydra:
        1) Inbound - for initial connection and investigation of data sources  
        2) Outbound - for efficient bulk transfer of selected data elements  
    These are designed for compatibility with the following technologies:  
        + Flat files (currently only CSV)  
        + IBM Notes (formerly Lotus Notes)  
        + SQL Alchemy - MSSQL & PostgreSQL  
        + Tableau Server Repository  
        + SAP (when integrated with 'SAPsucker')  
        + AWS - S3 & RDS  


### Setup  
In progress.
