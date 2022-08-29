# dime-cosas

Warehouse Extraction Process

```mermaid
flowchart LR
    id1(Lambda Process Manager) --> |Init Pipeline| id2[(Scraper Telegram)]
    id1(Lambda Process Manager) --> |Init Pipeline| id3[(Scraper Revolico)]
    
    id2[(Scraper Telegram)] --> id4(Orm Layer of Pipeline)
    id3[(Scraper Revolico)] --> id5(Orm Layer of Pipeline)
    
    id4(Orm Layer of Pipeline) --> |Save New Data| id6(MongoDB Document *Scraper Data Packege*)
    id5(Orm Layer of Pipeline) --> |Save New Data| id6(MongoDB Document *Scraper Data Packege*)
```


Warehouse Transformation Process

```mermaid
flowchart LR
    id1(Lambda Process Manager) --> |Init Pipeline| id2(Indexed Terms)
    id1(Lambda Process Manager) --> |Init Pipeline| id3(Theasaurus Build)
    
    id4(Orm Layer of Pipeline) --> |Load Scraper Data| id2(Indexed Terms)
    id5(Orm Layer of Pipeline) --> |Load Term List| id3(Theasaurus Build)
    
    id2(Indexed Terms) --> |Save Indexed Term| id4(Orm Layer of Pipeline)
    id2(Indexed Terms) --> |Query Expantion Process Update Event *Distpache Lambda Theasaurus Build*| id1(Lambda Process Manager) 
    id3(Theasaurus Build) --> |Save Theasaurus| id5(Orm Layer of Pipeline)
    
    id4(Orm Layer of Pipeline) --> |Read Scraper Data| id6(MongoDB Document *Scraper Data Packege*)
    id4(Orm Layer of Pipeline) --> |Write Indexed Term| id7(MongoDB Document *IndexedTerm Packege*)
    id5(Orm Layer of Pipeline) --> |Read Term List| id7(MongoDB Document *IndexedTerm Packege*)
    id5(Orm Layer of Pipeline) --> |Save Theasaurus| id8(MongoDB Document *Theasaurus Packege*)
```

Warehouse Load Process

```mermaid
flowchart LR
    id1(Client) --> |Query| id2(Theasaurus Query Expantion)
  
    id2(Theasaurus Query Expantion) --> id3(Orm Layer of Pipeline)
        
    id3(Orm Layer of Pipeline) --> id4(MongoDB Document *Theasaurus Packege*)
        
    id2(Theasaurus Query Expantion) --> |New Query| id5(Probabilistic Model)
    id5(Probabilistic Model) --> id6(Orm Layer of Pipeline)
        
    id6(Orm Layer of Pipeline) --> id7(MongoDB Document *IndexedTerm Packege*)
    id5(Probabilistic Model) --> |Ranking| id1(Client)
 
