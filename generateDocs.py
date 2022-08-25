from os import walk
import shutil
# get files and create docs 

def generatedocs(title,fileList):
    AppendtoSummaryFile(title=title)
    for file in fileList:
        markdownFile = open(file['path'],"r")
        newpath = 'documentation/src/' + file['path']
        markdownFileLines = markdownFile.readlines()
        AppendtoSummaryFile(fileName= file['name'],path = file['path'],heading=file['heading'])
        newMarkdown = open(newpath,"w")
        newMarkdown.write("")
        newMarkdown.close()
        newMarkdown = open(newpath,"a")
        for lines in markdownFileLines:
            newMarkdown.write(lines)
        newMarkdown.close()

    print(title + "  section is completed")

def AppendtoSummaryFile(**data):
    if 'title' in data:
        summaryFile = open("documentation/src/SUMMARY.md","a")
        summaryFile.write(data['title'])

       
    else: 
            summaryFile = open("documentation/src/SUMMARY.md","a")
            if data['heading'] == True:
                summaryFile.write('- ['+data['fileName'] +']'+ '('+data['path']+')'+'\n')
            else:
                summaryFile.write('     - ['+data['fileName'] +']'+ '('+data['path']+')'+'\n')
            
def WipeSummaryFile():
    summary = open("documentation/src/SUMMARY.md","w")
    summary.write("# summary\n")

def generateAssests(*paths):
    for path in paths:
        f = []
        for (dirpath, dirnames, filenames) in walk(path):
            f.extend(filenames)
            break
        
        
        for file in f:
            assetRelativePath = path + "/" + file
            newAssetPath = 'documentation/src/' + assetRelativePath
        
            shutil.copy(assetRelativePath,newAssetPath)
        
        
        print("Assests have been generated")



basicList = [
{
    'name': 'License', 
    'path': 'LICENSE.md', 
    'heading': True
},
{
    'name': 'About this Release', 
    'path': 'CHANGELOG.md', 
    'heading': True
},
{
    'name' :'How to contribute',
    'path' : 'support/guide/how_to_contribute.md',
    'heading' : True
},
{
    'name': 'Contributors', 
    'path': 'CONTRIBUTORS.md', 
    'heading': True
}


]

gettingStartedList = [
{
    'name': ' Jaseci Overview', 
    'path': 'support/guide/getting_started/introduction.md', 
    'heading': True
},
{
    'name': ' Installing Jaseci',
    'path': 'support/guide/getting_started/installation.md', 
    'heading': True
},
{
    'name': ' Setting up your Code Editor', 
    'path': 'support/guide/getting_started/setting_up_your_editor.md', 
    'heading': True
},
{
    'name': ' Writing your first app', 
    'path': 'support/guide/getting_started/writing_your_first_app.md', 
    'heading': True
},
{
    'name': ' Understanding JAC Programs', 
    'path': 'support/guide/getting_started/understanding_jac_programs.md', 
    'heading': True
}

]

LanguageGuide = [
    {
        'name': 'An Overview of the JAC Language', 
        'path': 'support/guide/jac_language_guide/jac_language_overview.md', 
        'heading': True
    },

    {
        'name': ' JAC Grammar', 
        'path': 'support/guide/jac_language_guide/jac_grammar.md', 
        'heading': True
    },

    {
        'name': ' keywords', 
        'path': 'support/guide/jac_language_guide/keywords.md', 
        'heading': True
    },

    {
        'name': ' Operators', 
        'path': 'support/guide/jac_language_guide/operators.md', 
        'heading': True
    },
    {
        'name': ' Control Flow', 
        'path': 'support/guide/jac_language_guide/control_flow.md', 
        'heading': True
    },
    {
        'name': ' Collections', 
        'path': 'support/guide/jac_language_guide/collections.md',
        'heading': True
    },
    {
        'name': ' Nodes', 
        'path': 'support/guide/jac_language_guide/nodes.md', 
        'heading': True
    },
    {
        'name': ' Edges',
        'path': 'support/guide/jac_language_guide/edges.md',
        'heading': True
    },
    {
        'name': ' Graphs', 
        'path': 'support/guide/jac_language_guide/graphs.md', 
        'heading': True
    },
    {
        'name': ' Walkers', 
        'path': 'support/guide/jac_language_guide/walkers.md', 
        'heading': True
    },
    {
        'name': ' Traversing a Graph', 
        'path': 'support/guide/jac_language_guide/traversing_a_graph.md', 
        'heading': False
    },
    {
        'name': ' Referencing a Node in Context', 
        'path': 'support/guide/jac_language_guide/referencing_node_context.md', 
        'heading': False
    },
    {
        'name': ' Passing Arguments', 
        'path': 'support/guide/jac_language_guide/passing_arguments.md', 
        'heading': True
    },
    {
        'name': ' Specifying Operating Context', 
        'path': 'support/guide/jac_language_guide/specifying_operating_context.md', 
        'heading': True
    },
    {
        'name': ' Actions in Jaseci', 
        'path': 'support/guide/jac_language_guide/actions.md', 
        'heading': True
    },
    {
        'name': ' Date Actions', 
        'path': 'support/guide/jac_language_guide/date_actions.md', 
        'heading': False
    },
    {
        'name': ' File Actions', 
        'path': 'support/guide/jac_language_guide/file_actions.md', 
        'heading': False
    },
    {
        'name': ' Net Actions', 
        'path': 'support/guide/jac_language_guide/net_actions.md', 
        'heading': False
    },
    {
        'name': ' Rand Actions', 
        'path': 'support/guide/jac_language_guide/rand_actions.md', 
        'heading': False
    },
    {
        'name': ' Request Actions', 
        'path': 'support/guide/jac_language_guide/request_actions.md', 
        'heading': False
    },
    {
        'name': ' Standard Actions', 
        'path': 'support/guide/jac_language_guide/standard_actions.md', 
        'heading': False
    },
    {
        'name': ' Vector Actions', 
        'path': 'support/guide/jac_language_guide/vector_actions.md', 
        'heading': False
    },
    {
        'name': ' Jaseci Actions', 
        'path': 'support/guide/jac_language_guide/jaseci_actions.md', 
        'heading': False
    }
]



samples_and_tutorials = [
    {
        'name' :'API Development',
        'path' : 'examples/api_development/README.md',
        'heading' : True
    },
      {
        'name' :'CanoniCAI',
        'path' : 'examples/canoniCAI/readme.md',
        'heading' : True
    },
    {
        'name' :'Adding a competency',
        'path' : 'examples/canoniCAI/documentation/add_competency.md',
        'heading' : False
    },
    {
        'name' :'Adding a following up state',
        'path' : 'examples/canoniCAI/documentation/add_followup_state.md',
        'heading' : False
    },
     {
        'name' :'Building FAQ States',
        'path' : 'examples/canoniCAI/documentation/add_followup_state.md',
        'heading' : False
    },
     {
        'name' :'Fixing Utterance',
        'path' : 'examples/canoniCAI/documentation/fixing_utterances.md',
        'heading' : False
    },
    {
        'name' :'Setting up a Custom Module',
        'path' : 'examples/canoniCAI/documentation/jaseci_actions_load_local.md',
        'heading' : False
    },

     {
        'name' :'NER Examples',
        'path' : 'examples/ner_examples/README.md',
        'heading' : True
    },

]

libraryReference = [
    {
        'name' :'Jaseci Kit',
        'path' : 'jaseci_kit/README.md',
        'heading' : True
    },
    {
        'name' :'Encoders',
        'path' : 'jaseci_kit/modules/encoders/README.md',
        'heading' : True
    },
    {
        'name' :'USE Encoder',
        'path' : 'jaseci_kit/modules/encoders/use_enc/README.md',
        'heading' : False
    },
    {
        'name' :'USE QA',
        'path' : 'jaseci_kit/modules/encoders/use_qa/README.md',
        'heading' : False
    },
    {
        'name' :'FastText',
        'path' : 'jaseci_kit/modules/encoders/fast_enc/README.md',
        'heading' : False
    },
    {
        'name' :'Bi-Encoder',
        'path' : 'jaseci_kit/modules/encoders/bi_enc/README.md',
        'heading' : False
    },
    {
        'name' :'Entity Recongition',
        'path' : 'jaseci_kit/modules/entity_utils/README.md',
        'heading' : True
    },
    {
        'name' :'Flair NER',
        'path' : 'jaseci_kit/modules/entity_utils/flair_ner/README.md',
        'heading' : False
    },
    {
        'name' :'Transformer NER',
        'path' : 'jaseci_kit/modules/entity_utils/tfm_ner/README.md',
        'heading' : False
    },
     {
        'name' :'LSTM NER',
        'path' : 'jaseci_kit/modules/entity_utils/lstm_ner/README.md',
        'heading' : False
    },
     {
        'name' :'Text Summarization',
        'path' : 'jaseci_kit/modules/summarization/README.md',
        'heading' : True
    },
    {
        'name' :'CL Summarization',
        'path' : 'jaseci_kit/modules/summarization/cl_summer/README.md',
        'heading' : False
    },
     {
        'name' :'T5 Summarization',
        'path' : 'jaseci_kit/modules/summarization/t5_sum/README.md',
        'heading' : False
    },
    {
        'name' :'Text Processing ',
        'path' : 'jaseci_kit/modules/text_processing/README.md',
        'heading' : True
    },
     {
        'name' :'Text Segmenter',
        'path' : 'jaseci_kit/modules/text_processing/text_seg/README.md',
        'heading' : False
    },
    {
        'name' :'Object Detection',
        'path' : 'jaseci_kit/modules/object_detection/README.md',
        'heading' : True
    },
    {
        'name' :'YOLO V5',
        'path' : 'jaseci_kit/modules/object_detection/yolo_v5/README.md',
        'heading' : False
    },
    {
        'name' :'Non-AI Tools',
        'path' : 'jaseci_kit/modules/non_ai/README.md',
        'heading' : True
    },
    {
        'name' :'PDF Extractor',
        'path' : 'jaseci_kit/modules/non_ai/pdf_ext/README.md',
        'heading' : False
    },

    {
        'name' :'Jaseci Core',
        'path' : 'jaseci_core/README.md',
        'heading' : True
    },


]

jaseci_webkit = [

    {
        'name' :'Webkit Components',
        'path' : 'jaseci_ui_kit/docs/components.md',
        'heading' : True
    },
      {
        'name' :'Types of Components',
        'path' : 'jaseci_ui_kit/docs/typesOfComponents.md',
        'heading' : True
    }

]

def main(basicList,gettingStartedList,LanguageGuide,samples_and_tutorials,libraryReference,jaseci_webkit):
    WipeSummaryFile()
    generatedocs('# Jaseci Offical Documentation \n',basicList)
    generatedocs('# Getting Started \n',gettingStartedList)
    generatedocs('# The JAC Programming Language Guide \n',LanguageGuide)
    generatedocs('# Samples and Tutorials \n',samples_and_tutorials)
    generatedocs('# Jaseci Library Reference \n',libraryReference)
    generatedocs('# Jaseci webkit \n',jaseci_webkit)




main(basicList,gettingStartedList,LanguageGuide,samples_and_tutorials,libraryReference,jaseci_webkit)