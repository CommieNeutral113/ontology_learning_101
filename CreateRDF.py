import os
import pandas as pd

def generator(filename, relation_df:pd.DataFrame, ner_df: pd.DataFrame, term_df: pd.DataFrame):
    rdf_text = f'''<?xml version="1.0"?>
<rdf:RDF xmlns="http://www.semanticweb.org/long/ontologies/2023/10/{filename}#"
     xml:base="http://www.semanticweb.org/long/ontologies/2023/10/{filename}"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:xml="http://www.w3.org/XML/1998/namespace"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
    <owl:Ontology rdf:about="http://www.semanticweb.org/long/ontologies/2023/10/{filename}"/>
    


    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Annotation properties
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->
    
    

'''
    # Define relation
    Annotation_properties = ''''''
    relation_list = list(set(relation_df['relation'].values.tolist()))
    for i in range(len(relation_list)):
        relation = relation_list[i]
        relation = relation.replace(' ', '_')
        # print(relation)
        Annotation_properties += f'''    <!-- http://www.semanticweb.org/long/ontologies/2023/10/{filename}#{relation} -->

    <owl:AnnotationProperty rdf:about="http://www.semanticweb.org/long/ontologies/2023/10/{filename}#{relation}"/>
    


''' 
    
    rdf_text += Annotation_properties

    # Define Class

    rdf_text += '''    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Classes
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


'''

    Classes = ''''''

    class_list = list(set(ner_df['Label'].values.tolist()))
    for ner_class in class_list:
        Classes += f'''    <!-- http://www.semanticweb.org/long/ontologies/2023/10/{filename}#{ner_class} -->

    <owl:Class rdf:about="http://www.semanticweb.org/long/ontologies/2023/10/{filename}#{ner_class}"/>
    


'''
        
    rdf_text += Classes

    # Define Entity
    rdf_text += '''    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Individuals
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->

    


'''
    Entities = ''''''
    subject_list = relation_df['subject'].values.tolist()
    entities_has_class = ner_df['Entity'].values.tolist()
    terms = term_df['Term'].values.tolist()
    entities = list(set(entities_has_class + terms + subject_list))

    for entity in entities:
        Entities += f'''    <!-- http://www.semanticweb.org/long/ontologies/2023/10/{filename}#{entity.replace(' ', '_')} -->

    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/long/ontologies/2023/10/{filename}#{entity.replace(' ', '_')}">
'''
        if (entity in entities_has_class):
            row = ner_df.loc[ner_df['Entity'] == entity]
            entity_class = row['Label'].values[0].replace(' ', '_')
            Entities += f'''        <rdf:type rdf:resource="http://www.semanticweb.org/long/ontologies/2023/10/{filename}#{entity_class}"/>
'''
        if (entity in subject_list):
            rows = relation_df.loc[relation_df['subject'] == entity]
            for index in range(len(rows)):
                row = rows.iloc[index]         
                relate_to = row['relation'].replace(' ', '_')
                object_related = row['object'].replace(' ', '_')
                Entities += f'''        <{relate_to} rdf:resource="http://www.semanticweb.org/long/ontologies/2023/10/{filename}#{object_related}"/>
'''


        Entities += '''    </owl:NamedIndividual>
'''

    rdf_text += Entities

    # End
    rdf_text += '''</rdf:RDF>



    <!-- Generated by the OWL API (version 4.5.9.2019-02-01T07:24:44Z) https://github.com/owlcs/owlapi -->''' 

    path = 'RDF_file/' + filename

    if (os.path.exists('RDF_file/' + filename + '.owl')):
        os.remove('RDF_file/' + filename + '.owl')

    # print (rdf_text)
    # path = 'RDF_file/' + filename + '.txt'
    with open(path + '.txt', 'w') as file:
        file.write(rdf_text)
        file.close()
    
    os.rename(path + '.txt', path + '.owl')
