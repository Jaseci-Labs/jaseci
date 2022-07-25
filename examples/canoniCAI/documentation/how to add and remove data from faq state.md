# How to add and remove data from faq state

##### Table of Contents  
- [ Introduction ](#introduction)
- [How to add data from faq state](#step-1-how-to-add-data-from-faq-state)
- [How to remove data from faq state](#step-2-how-to-remove-data-from-faq-state)

# Introduction
In this section we will be teaching you how to add and remove datat from graph from the faq state.

# Step 1: How to add data from faq state
The steps are as follows:
* run jaseci console: ``` jsctl -m ```
* load all the actions required: ``` actions load module [module] ```
* builing the application using:  ``` jac build main.jac ```
* registering the sentinel: ``` sentinel register -set_active true -mode ir main.jir ```
* delete any graph if exists: ``` graph delete active:graph ```
* create the graph: ``` graph create -set_active true ```
* run init walker: ``` walker run init ```
* run read walker which will add the data to the faq state: ``` walker run read -ctx "{\"source_url\": \"https://www.yum.com/wps/portal/yumbrands/Yumbrands/company/our-brands/kfc\"}" ```

# Step 2: How to remove data from faq state
To delete data you will have to run the forget walker, run the first 7 steps from step 1 then follow the next step as follows:
* run forget walker: ``` walker run forget ```
