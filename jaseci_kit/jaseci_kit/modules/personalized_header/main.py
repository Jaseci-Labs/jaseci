### PH Start
'''
TODO: Personalized Header Initialization. (create_header)

Args: 
---- YAML file for the personal header architecture : str
---- output_type: str ('tensor'/'list') - this will be helpful if are compounding more than 2 modules
---- Location to the weights : str
Return:
---- ph object

Remarks: Weights will not be loaded yet. Only the Model structure will be loaded.
'''

''' (PH Object Method)
TODO: forward propogation. (forward)

Args:
---- input: tensor/list
Return:
---- output: output_type

Remarks: Weights will be loaded oncall of predict. Allowing multiple users to use the service again and again
'''

'''(PH Object Method)
TODO: backward propogation. (backward)
'''
### PH End

### Module Compositor Start
'''
TODO: Compositor creator (create_composite)

Args:
---- List of Modules: list
---- parameters: list<dict>
'''

'''
TODO: predict (predict)

Args:
---- input
Return:
---- output
'''

'''
TODO: train (train)

Args:
---- dataset
'''
### Module Compositor End

# action load compositor
# can compositor.create_composite

# create_compistor([use_enc, personalized_header],["", {
#     yaml:
#     ajdnas:
# }])
# compositor.predict('user_1', input) --> output;
# compositor.train(dataset, user_1);

# similar image ---> text ----> image
# image, imge2