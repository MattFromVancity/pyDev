from DynamicLabels import DynamicLabel

#Region specific language code
region_lang = "fr"
#source language code
english_code = "en-US"
#List of Labels
listOfNamedLabels = ["Dog","Cat","Car","Fish"]
#Google Project Id
google_project_id = "<Enter Your Google Project Id>"


#Predicated label index (output of model)
predLabel = 2

#Create an instance of dynamic labels
dynamicLabelObj = DynamicLabel(listOfNamedLabels, google_project_id, english_code)

#Finding out all the different languages we can translate to
dynamicLabelObj.printLanguageCodes()

#Getting the translated version of the index based label
convertedLabel = dynamicLabelObj.getDynamicLabel(predLabel,region_lang)

print(convertedLabel)