/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {

  Started: {

    'Introduction': [
      'getting-started/getting-to-know-jaseci',
      'getting-started/installation',
      'getting-started/set-up-editor',
      'getting-started/first-app',
      {
        type: 'category',
        label: 'JAC Language Overview',
        items: ['getting-started/JAC-Language-Overview/how', 'getting-started/JAC-Language-Overview/controlflow', 'getting-started/JAC-Language-Overview/ModelStructures', 'getting-started/JAC-Language-Overview/ModelBehaivour', 'getting-started/JAC-Language-Overview/operatingContext', 'getting-started/JAC-Language-Overview/passingArguments', 'getting-started/JAC-Language-Overview/report', 'getting-started/JAC-Language-Overview/nodeCommuniation', 'getting-started/JAC-Language-Overview/take']
      }


    ]
  },

  Developing: {

    'Developing with JAC': [
      'Developing_with_JAC/Overview',
      {
        type: 'category',
        label: 'Language Features',
        items: ['Developing_with_JAC/Language_Features/input_output', 'Developing_with_JAC/Language_Features/dataTypes', 'Developing_with_JAC/Language_Features/Operator', 'Developing_with_JAC/Language_Features/ControlFlow', 'Developing_with_JAC/Language_Features/FileHnadling', 'Developing_with_JAC/Language_Features/OOP', {
          type: 'category',
          label: 'Acion Modules',
          items: ['Developing_with_JAC/Language_Features/actions/date', 'Developing_with_JAC/Language_Features/actions/file', 'Developing_with_JAC/Language_Features/actions/net', 'Developing_with_JAC/Language_Features/actions/rand', 'Developing_with_JAC/Language_Features/actions/request', 'Developing_with_JAC/Language_Features/actions/std', 'Developing_with_JAC/Language_Features/actions/vectors', 'Developing_with_JAC/Language_Features/actions/jaseci'],
        },]
      },
      'Developing_with_JAC/Design_Philosophy_and_Patterns',
      'Developing_with_JAC/Testing_and_Degugging',
      'Developing_with_JAC/API_Development'
    ]
  },

  Tools: {

    'Jaseci Tools': [
      'Tools_and_Features/Overview',
      'Tools_and_Features/Jaseci_Serv',
      'Tools_and_Features/Jaseci_Studio',
      'Tools_and_Features/VScode_PLugins'

    ],

    'Jaseci Kit': [
      'Tools_and_Features/Jaseci_AI_Kit/Overview',
      {
        type: 'category',
        label: 'Encoders',
        items: ['Tools_and_Features/Jaseci_AI_Kit/useqa', 'Tools_and_Features/Jaseci_AI_Kit/encode', 'Tools_and_Features/Jaseci_AI_Kit/Biencoder', 'Tools_and_Features/Jaseci_AI_Kit/fastTestEconder']
      },
      {
        type: 'category',
        label: 'Entity',
        items: ['Tools_and_Features/Jaseci_AI_Kit/entityExtraction', 'Tools_and_Features/Jaseci_AI_Kit/entityExtractionTransformers']
      },
      {
        type: 'category',
        label: 'Summarization',
        items: ['Tools_and_Features/Jaseci_AI_Kit/cl_summer', 'Tools_and_Features/Jaseci_AI_Kit/t5Summarization']
      },
      {
        type: 'category',
        label: 'Text Processing',
        items: ['Tools_and_Features/Jaseci_AI_Kit/textSegement']
      },
      {
        type: 'category',
        label: 'Non AI tools',
        items: ['Tools_and_Features/Jaseci_AI_Kit/pdfExtractor']
      },

    ]

  },


  Samples: {

    'Sample Projects': [
      'Samples_and_Tutorials/Overview',
      'Samples_and_Tutorials/Recommender_System',
      'Samples_and_Tutorials/Conversational_AI_Application',

    ]

  },

  Resources: {

    'Resources': [
      'Resources/Architectural_Overview',
      'Resources/API_Reference',
      'Resources/FAQ',
      'Resources/appendix'

    ]

  }



};
module.exports = sidebars;
