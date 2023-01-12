# Jaseci Kit New Module CheckList

- [] Naming Convention
    * Name of the module and name of file should be same.
    * Provide reason if not.
- [] Tests
    * Should have a testing logic file <test_module_name> and test_data file
    * Test function for each API publicly available
    * 1 Test function for overall logic testing
- [] Update requirements.txt
    * `jaseci_ai_kit/requirements.txt` should have all the dependency used in the module
- [] Documentation
    * A readme file to demonstrate functionality usage
    * A developer documentation to help with future contribution from the community.
- [] A `<module_name>.py` file outside module that imports the main module
- [] Deployment manifest:
    * `<module_name>.yml` should be included in support/manifests
- [] Test and validate the module can be loaded as action through the three action load commands:
    * `action load module`
    * `action load local`
    * `action load remote`
