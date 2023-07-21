# maDMPs to support reviewers 2.0

## Introduction
This project was designed to facilitate the assessment and validation of machine-actionable Data Management Plans (*maDMPs*). The goal for this project is to aid the process of validation by utilizing *SHACL* constraints for validation and requirements definition. It should provide a more efficient and reliable way to assess *maDMPs* and ensure compliance with funder requirements.

In the past, the validation process heavily relied on *SPARQL* queries, which are often verbose and error-prone. However, with the emergence of *SHACL*, we now have a more robust technology for describing and validating *RDF* data. *SHACL* offers several benefits over alternative solutions, such as *ShEx* (Shape Expressions). It provides a rich set of built-in constraints, supports advanced validation rules, and offers better integration with the *RDF* data model. These advantages make *SHACL* an ideal choice for expressing constraints and requirements for *maDMPs* in a comprehensive and automated manner.

Existing validation implementation are improved by rewriting existing *SPARQL* queries, from the referenced paper for this project, as *SHACL* constraints and defining new constraints, where needed, based on funder requirements. By leveraging the power of *SHACL*, we aim to enhance the coverage of funder requirements and provide a more streamlined validation process for *maDMPs*.

This *README*/Report provides an overview of the tool, its methodology, usage instructions, and the results of the assessment conducted on *maDMPs* from the Data Stewardship community. It also discusses the limitations, challenges, and potential future enhancements of the tool.


## Project

This section outlines the methodology used and considerations made in the development of the maDMPs Assessment Project and describes the steps taken to validate and assess maDMPs, specifically through the use of *SHACL* constraints.

### Data Preprocessing

The first step in the process involved cleaning and preprocessing the *maDMPs*, that were fetched from *Zenodo*, provided in *JSON* format. Manual cleaning was performed to ensure the integrity and consistency of the data. During this cleaning process, the following issues were identified and resolved:
- `madmp5.json`:
    - Error at line 60: Extra comma
    - Error at line 147: Extra comma
    - Error at line 178: Extra comma
    - Error at line 393: Extra comma
- `madmp6.json`:
    - Error at line 58: Extra comma
    - Error at line 98: Extra comma
- `madmp8.json`:
    - Error at line 36: Misformatted string and extra comma
    - Same error at line 96

Additionally, `madmp12.json` was skipped purposefully due to it lacking a proper structure throughout the whole document and also because it was so little in terms of information. It was labelled as `skip_madmp12.json` to distinguish it. All original `madmps` can be found under the folder **madmps**.

Once the cleaning process was complete, the *JSON maDMPs* were transformed into *JSON-LD* format using the script `json_ld_converter.py`. During this process, it was realized that some property fields were missing in the context mappings, so they were updated to include the `preservation_statement`, `is_reused`, `methodology` and `methodology_id` fields. The mappings that were used in the script can be found under the **mappings** folder and they were extracted from a repository that was mentioned in the reference paper. This repository is from a researcher at the TU, and it can be found [here](https://github.com/fekaputra/dcso-json). As for the paper that was used as reference in this project, it can be found [here](https://repository.publisso.de/resource/frl:6430058/data). Lastly the resulting *JSON-LD madmps* can all be found in the **output** folder.

### Constraint Definition

The majority of the work was done for this section. To validate the *maDMPs*, a set of constraints based on the evaluation rubric provided by *Science Europe*, which can be found [here](https://www.scienceeurope.org/media/4brkxxe5/se_rdm_practical_guide_extended_final.pdf), were defined. The existing *SPARQL* queries, which were pulled from the reference paper's repository, previously used for validation, were transformed into *SHACL* constraints. This process was done manually and based on online documentation, which can be found [here](https://www.w3.org/TR/shacl/). The *SPARQL* queries were pulled from [here](https://github.com/raffaelfoidl/maDMP-evaluation/tree/v1.2/queries) and were copied into this project repository under the **original_queries** folder. To ensure the quality of the *SPARQL* queries and if the pre-processing, specifically the *.jsonld* *madmps*, were accurate, they were tested and applied in a *GraphDB* repository. The *SHACL* constraints were made to cover the required funder criteria and facilite future automated validation processes. These constraint stayed true to the original reference *SPARQL* queries and were improved upon where necessary to fit the rubric requirements more adequately. The *SHACL* constraints can be found under the folder **shacl_constraints** and follow the same naming convention as their reference *SPARQL* queries. This naming convention is based on the evaluation rubric, pages 34-49, and stems from the subpoints e.g. point *1b)* would match the constraints `shapes_1b1.ttl` and `shapes_1b2.ttl`. Some extra constraints were added that weren't there in the original queries, i.e. `shapes_1a.ttl`, and some constraints were applied more strictly than the queries or maybe even less at times. Not all constraints could be strictly due to several reasons, and these are: if the constraints would be followed strictly addressed most *maDMPs* here would not validate at all, if not all; the source mappings are not complete will all the rubrics requirement and I could only add the ones manually that I noticed, meaning some might have been missed. 

### Constraint Application and Validation

Once the *SHACL* constraints were defined, they were applied to the *maDMPs* from the Data Stewardship community. The *maDMPs* were validated against the set of constraints to determine their compliance. The validation process aimed to identify any violations or areas of improvement within the *maDMPs*. To facilitate this step, a custom constraint checker was developed, see `constraints_checker.py`. The constraint checker utilized the *SHACL* validation engine and provided accurate and informative validation results. For this project *GraphDB* was also used, as already mentioned, but its constraint validation was lackluster and the logging was obscure and not as well understandable as the one made here. The constraints and *madmps*  do conform for *GraphDB* implementation though, meaning one should be able to apply them there as well.

## Repository Structure
- **madmps** : Contains the machine-actionable Data Management Plans (maDMPs) fetched from Zenodo.

- **mappings** : Holds the context mappings used for converting maDMPs from JSON to JSON-LD format.
- **original_queries** : Contains the original SPARQL queries used for filtering relevant information from the maDMPs.
- **output** : Stores the assessment results, validation reports, and other output files.
- **shacl_constraints** : Contains the SHAPEL constraints used for maDMP validation.
- `constraints_checker.py` : A Python script to apply the SHAPEL constraints and perform validation.
- `json_ld_converter.py` : A script to convert *JSON maDMPs* to *JSON-LD* format.
- *README.md* : Provides an overview of the project, methodology, and usage instructions.
- *requirements.txt* : Lists the required dependencies and packages for running the assessment tool.

## Usage

**Environment Setup**:
- Make sure you have *Python* installed (version 3.11)
- Clone the repository and navigate to the project directory:

    `git clone https://github.com/your-username/maDMPs-assessment-tool.git
    cd maDMPs-assessment-tool`
- Install the required dependencies:

    `pip install -r requirements.txt`

Once the environment is set up, you can utilize the following scripts:

- `json_ld_converter.py`: Use this script to convert new *JSON maDMPs* to *JSON-LD* format. This step is only necessary if you have new *JSON maDMPs* that haven't been converted yet. The converted *maDMPs* will be saved in the **output** directory as *JSON-LD* files.

- `constraints_checker.py`: Use this script to apply *SHACL* constraints to the *maDMPs*. The script will validate the *maDMPs* against the defined constraints and generate validation reports.

## Report and Results
The assessment of maDMPs was conducted based on the evaluation rubric provided by *Science Europe* and prior *SPARQL* queries. The table below presents the rubric requirements and the corresponding *maDMPs* that fulfill each requirement:

| Rubric Requirement | Relevant SHACL Constraints | Fulfilling maDMPs |
|--------------------|---------------------------|------------------|
| General Information      | `shapes_01.ttl`| All *maDMPs* 
| General Information      | `shapes_02.ttl` | `madmp6.jsonld`, `madmp7.jsonld`
| General Information     | `shapes_03.ttl` | All *maDMPs* 
| 1a)      | `shapes_1a.ttl` | `madmp8.jsonld`, `madmp9.jsonld`
| 1b)      | `shapes_1b1.ttl`, `shapes_1b2.ttl`, `shapes_1b3.ttl` | All *maDMPs* 
| 2a)      | `shapes_2a1.ttl` | All *maDMPs* besides `madmp1.jsonld`
| 2a)      | `shapes_2a2.ttl` | All *maDMPs*
| 2a)      | `shapes_2a3.ttl` | `madmp2.jsonld`, `madmp3.jsonld`, `madmp5.jsonld`, `madmp6.jsonld`, `madmp7.jsonld`, `madmp8.jsonld`, `madmp10.jsonld`
| 2a)      | `shapes_2a4.ttl` | All *maDMPs*
| 2b)      | `shapes_2b.ttl` | All *maDMPs*
| 3a)      | `shapes_3a.ttl` | All *maDMPs*
| 3b)      | `shapes_3b1.ttl` | No *maDMPs*
| 3b)      | `shapes_3b2.ttl` | All *maDMPs*
| 4a)      | `shapes_3b2.ttl` | All *maDMPs* (since no fitting context, this is the closest to its actual constraint, but it has nothing to do with actually enforcing the definition of how data is processed)
| 4b)      | No fitting context, therefore no fitting constraints | None since not applied
| 4c)      | `shapes_4c1.ttl`, `shapes_4c2.ttl` | All *maDMPs*
| 5a)      | `shapes_5a1.ttl` | `madmp8.jsonld`, `madmp9.jsonld`, `madmp10.jsonld`, `madmp11.jsonld`
| 5a)      | `shapes_5a2.ttl` | `madmp5.jsonld`, `madmp8.jsonld`, `madmp10.jsonld`
| 5a)      | `shapes_5a3.ttl` | All *maDMPs* besides `madmp11.jsonld`
| 5b)      | `shapes_5b.ttl` | `madmp3.jsonld`, `madmp5.jsonld`, `madmp6.jsonld`, `madmp7.jsonld`
| 5c)      | `shapes_5c.ttl` | `madmp1.jsonld`, `madmp5.jsonld`, `madmp8.jsonld`, `madmp9.jsonld`, `madmp10.jsonld`, `madmp11.jsonld`
| 5d)      | `shapes_5d1.ttl` | `madmp1.jsonld`, `madmp5.jsonld`, `madmp8.jsonld`, `madmp9.jsonld`, `madmp10.jsonld`, `madmp11.jsonld`
| 5d)      | `shapes_5d2.ttl` | `madmp2.jsonld`, `madmp3.jsonld`, `madmp4.jsonld`, `madmp5.jsonld`, `madmp6.jsonld`, `madmp7.jsonld`, `madmp8.jsonld`, `madmp9.jsonld`
| 6a)      | `shapes_6a1.ttl` | All *maDMPs*
| 6a)      | `shapes_6a2.ttl` | `madmp1.jsonld`, `madmp2.jsonld`, `madmp4.jsonld`, `madmp5.jsonld`, `madmp8.jsonld`, `madmp9.jsonld`, `madmp11.jsonld`
| 6b)      | `shapes_6b1.ttl` | `madmp2.jsonld`, `madmp3.jsonld`, `madmp6.jsonld`, `madmp7.jsonld`, `madmp8.jsonld`, `madmp9.jsonld`, `madmp10.jsonld`
| 6b)      | `shapes_6b2.ttl` | All *maDMPs* besides `madmp11.jsonld`


The assessment of the *maDMPs* using *SHACL* constraints indicates varying degrees of compliance. While some requirements were well met, there are areas for improvement. The use of *SHACL* constraints facilitated an automated and standardized validation process, aiding reviewers in their assessment. Applying *SHACL* constraints instead of *SPARQL* queries allows to automatically enforce *maDMPs* to adhere instead of simply querying them about if they conform or not.

### Differences between Constraint and Queries

Here, the differences between the constraints and queries are briefly mentioned. Even when it is describes as *"Kept true to the SPARQL query"*, one should be aware that of course there are still different and have different effects since one queries whereas the other applies a constraint or requires something from the *maDMP*.

| Relevant SHACL Constraints | Relevant SPARL Query | Considerations/Alterations in SHACL vs. SPARQL|
|--------------------|---------------------------|------------------|
|`shapes_01.ttl`| `0-1.sparql`| Only hasContact is mandatory, the exact constellation of it is open |
|`shapes_02.ttl`| `0-2.sparql`| Only applied the constraint didn't apply default values since we want this constraint to fail if fields do not exist |
|`shapes_03.ttl`| `0-3.sparql`| Funding is explicitly optional due to self-funded projects, but requires ID if existing|
|`shapes_1a.ttl`| *None* | Not covered by SPARQL and introduced as SHACL |
|`shapes_1b1.ttl`| `1-b-1.sparql`| Kept true to the SPARL query besides enforcing literal datatype|
|`shapes_1b2.ttl`| `1-b-2.sparql`| Kept true to the SPARL query besides omitting default values|
|`shapes_1b3.ttl`| `1-b-3.sparql`| Kept true to the SPARL query besides omitting default values |
|`shapes_2a1.ttl`| `2-a-1.sparql`| Kept true to the SPARL query|
|`shapes_2a2.ttl`| `2-a-2.sparql`| SHACL only ensures that the hasDataset property exists, along title and keyword|
|`shapes_2a3.ttl`| `2-a-3.sparql`| Kept true to the SPARL query|
|`shapes_2a4.ttl`| `2-a-4.sparql`| Kept true to the SPARL query|
|`shapes_2b.ttl`| `2-b-1.sparql`| Kept true to the SPARL query besides enforcing literal datatype|
|`shapes_3a.ttl`| `3-a-1.sparql`| Kept true to the SPARL query besides enforcing literal datatype (aside from IRI to avoid constraint failures due to format issues, but it should be enforced in reality)|
|`shapes_3b1.ttl`| `3-b-1.sparql`| To fully match the rubric, description was made mandatory and title optional (since no explicit mention, but it should be mandatory too in reality)|
|`shapes_3b2.ttl`| `3-b-2.sparql`| Defined expected strings, anything else besides that would result in it failing constraint and again enforced literal type|
|`shapes_4c1.ttl`| `4-c-1.sparql`| Kept true to the SPARL query besides expanding with answer "no"|
|`shapes_4c2.ttl`| `4-c-2.sparql`| Stricter and more encompassing than SPARQL query |
|`shapes_5a1.ttl`| `5-a-1.sparql`| Removed format from being required as it was not explicitly mentioned in the rubric section|
|`shapes_5a2.ttl`| `5-a-2.sparql`| Preservation statement has to exist at least once|
|`shapes_5a3.ttl`| `5-a-3.sparql`| Stricter constraint besides ommitting sensitive data since it is not covered in this rubric section|
|`shapes_5b.ttl`| `5-b-1.sparql`| Kept true to the SPARL query|
|`shapes_5c.ttl`| `5-c-1.sparql`| Kept true to the SPARL query|
|`shapes_5d1.ttl`| `5-d-1.sparql`| Kept true to the SPARL query|
|`shapes_5d2.ttl`| `5-d-2.sparql`| Kept true to the SPARL query|
|`shapes_6a1.ttl`| `6-a-1.sparql`| Made role already mandatory in this constraint|
|`shapes_6a2.ttl`| `6-a-2.sparql`| Made this constraint a subset of `shapes_6a1.ttl`|
|`shapes_6b1.ttl`| `6-b-1.sparql`| Stricter and more encompassing than SPARQL query|
|`shapes_6b2.ttl`| `6-b-2.sparql`| Stricter and more encompassing than SPARQL query|
## Further Opportunities & Limitations

Hopefully this has provided valuable insights into the validation and assessment of *maDMPs* using *SHACL* constraints. However, there are certain limitations and further opportunities to consider.

One limitation is the lack of testing with *ShEx* (Shape Expressions) constraints. This is due to the fact that initially, the intention was to validate *maDMPs* solely through *GraphDB*, which did not support *ShEx* validation. This limitation highlights an area for improvement in future iterations of the tool, where both *SHACL* and *ShEx* constraints can be explored for comprehensive validation.

Another consideration is the relaxed nature of the constraints applied. Strict constraints were not enforced in this exercise to allow for a broader range of *maDMPs* to adhere to the requirements. It is important to keep in mind that the constraints provided should ideally serve as guidelines and recommendations rather than rigid rules. Additionally, one should regard as these constraints as showcases what can be done with *SHACL* instead of how *maDMPs* ought to conform.

Due to time constraints and individual work on the project, explicit explanations of the *SHACL* constraints and the rationale behind the choices made were not provided. However, it is anticipated that *SHACL* constraints offer a more concise and understandable representation compared to complex *SPARQL* queries, making them easier to comprehend and interpret independently.

## License

This project is released under the **MIT License**. This means that you are free to use, modify, and distribute the tool for both commercial and non-commercial purposes. However, please note that the tool is provided as-is, without any warranties or guarantees.

By using the *maDMPs Assessment Tool*, you agree to the terms and conditions of the **MIT License**.