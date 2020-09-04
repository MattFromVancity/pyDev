from google.cloud import translate
from google.cloud import translate_v2 
from exceptionHandle import InvalidLanguageCode, TranslationError

def googleTranslate(inputText, target_lang, source_lang, p_id):
    """
    Utilizies the Google Cloud Translate API to translate inputText

    Attributes:
        inputText (str) - text to be translated
        target_lang (str) - target language code for translation 
        source_lang (str) - source language code for translation
        p_id (str) - Google project id

    Return parameters:
        (list) of translation objects
    """

    translate_client = translate.TranslationServiceClient()

    location = "global"
    project_id = p_id

    parent = f"projects/{project_id}/locations/{location}"

    #Obtain the translations results via the Google Cloud Translation API
    result = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [inputText],
            "mime_type": "text/plain",
            "source_language_code": source_lang,
            "target_language_code": target_lang 
        }
    )

    return result.translations
 
class DynamicLabel:
    """Class for translating an indexed label from a machine learning model to a language specific label.
    
    Dependecies:
        Google Cloud SDK -- https://cloud.google.com/sdk/docs
        Google Cloud Config. Authentication -- https://cloud.google.com/docs/authentication/getting-started
    """

    def __init__(self, labels, project_id, base_lang):
        """Sets the members of a DynamicLabel object (Constructor)

        Attributes:
            base_lang (string) - langauge code supported found through printLanguageCodes()
            project_id (string) - Google project id
            labels (list/array) - array of strings repersenting indexed labels
    
        Return parameters:
            None
        """

        self.base_lang = base_lang
        self.labels = labels
        self.project_id = project_id
        self.lang_codes = dict()
        #Set the local language codes
        for lang_inst in self.getAllAvaliableLangs():
            self.lang_codes[lang_inst['language']] = lang_inst['name']

    #Google API Call 
    @staticmethod
    def getAllAvaliableLangs():
        translate_client = translate_v2.Client()
        return translate_client.get_languages()

    def printLanguageCodes(self):
        """Print to the command line all conforming language codes supported by the Google Cloud Translate API

        Attributes:
            None
        
        Return parameters:
            None
        """

        for key in self.lang_codes:
            print(f"Use '{key}' for {self.lang_codes[key]}")

 
    def getDynamicLabel(self, labelIdx, target_lang_code):
        """Translates the label at self.labels[labelIdx] to the target_lang_code

        Attributes:
            labelIdx (int) - Range [0, max_length(self.labels))
            target_language (str) - Valid language code that conforms to Cloud API, use printLanguageCodes() method to obtain all
            supported languages and their codes
    
        Return parameters: 
            (str) - translated text 
        """

        #LabelIdx must be a valid index
        if(labelIdx >= len(self.labels) and labelIdx >= 0):
            raise IndexError
        
        #Check to ensure target_language conforms to Google API S
        try:
            self.lang_codes[target_lang_code]
        except KeyError:
            raise InvalidLanguageCode(target_lang_code)
        else:
            translations = googleTranslate(self.labels[labelIdx], target_lang_code, self.base_lang, self.project_id)

        if(len(translations) > 0):
            return translations[0].translated_text
        else:
            raise TranslationError("No possible translation.")
    
    def resetDynamicLabels(self, new_lang, new_labels):
        """
        Resets the object.labels data member to a new_lang based on new_labels

        Attributes:
            new_lang (str) - valid language code
            new_labels (list) - list of strings repersenting new labels

        Return parameters:
            None
        """

        try:
            self.base_lang = self.lang_codes[new_lang]
        except KeyError:
            print(f"RESET FAILED >> '{new_lang}' is not a valid language code.")
        else:
            self.base_lang = new_lang
            self.labels = new_labels