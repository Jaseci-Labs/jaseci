
module.exports = {

 Developing: {

  'Developing with JAC' : [
    'Developing_with_JAC/Overview',
    {
      type : 'category',
      label : 'Language Features',
      items : ['Developing_with_JAC/Language_Features/input_output','Developing_with_JAC/Language_Features/dataTypes','Developing_with_JAC/Language_Features/Operator','Developing_with_JAC/Language_Features/Operator']
    },
    'Developing_with_JAC/Language_Feature',
    'Developing_with_JAC/Design_Philosophy_and_Patterns',
    'Developing_with_JAC/Testing_and_Degugging',
    'Developing_with_JAC/API_Development'
  ]
 },

 Started: {
   
  'Introduction': [
     'getting-started/getting-to-know-jaseci',
     'getting-started/installation',
     'getting-started/set-up-editor',
     'getting-started/first-app',
     'getting-started/Jac-Language-Overview'


  ]
},

Tools: {

  'Jaseci Tools' : [
    'Tools_and_Features/Overview',
    'Tools_and_Features/Jaseci_Kit',
    'Tools_and_Features/Jaseci_Serv',
    'Tools_and_Features/Jaseci_Studio',
    'Tools_and_Features/VScode_PLugins'

  ],

  'Jaseci Kit' : [
    'Tools_and_Features/Jaseci_Kit/Overview',
    {
      type : 'category',
      label : 'Encoders',
      items : ['Tools_and_Features/Jaseci_Kit/useqa','Tools_and_Features/Jaseci_Kit/encode','Tools_and_Features/Jaseci_Kit/Biencoder','Tools_and_Features/Jaseci_Kit/fastTestEconder']
    },
    {
      type : 'category',
      label : 'Entity',
      items : ['Tools_and_Features/Jaseci_Kit/entityExtraction','Tools_and_Features/Jaseci_Kit/entityExtractionTransformers']
    },
    {
      type : 'category',
      label : 'Summarization',
      items : ['Tools_and_Features/Jaseci_Kit/cl_summer','Tools_and_Features/Jaseci_Kit/t5Summarization']
    },
    {
      type : 'category',
      label : 'Text Processing',
      items : ['Tools_and_Features/Jaseci_Kit/textSegement']
    },
    {
      type : 'category',
      label : 'Non AI tools',
      items : ['Tools_and_Features/Jaseci_Kit/textSegement']
    },

  ]

},

Samples : {

  'Sample Projects' : [
    'Samples_and_Tutorials/Overview',
    'Samples_and_Tutorials/Recommender_System',
    'Samples_and_Tutorials/Conversational_AI_Application',

  ]

}



};