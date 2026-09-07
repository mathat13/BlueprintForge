QuestionData Contract

Field                       Valid                                               Invalid
-----------------------------------------------------------------------------------------------------------------------------------
question                    string                                              null / non-string
summary                     string                                              null / non-string
reasoning                   object                                              null / absent
reasoning.status            string                                              null / absent
reasoning.worksheet_path    string / absent                                     wrong type
knowledge                   object / null / absent                              -
knowledge.type              string / (absent / null when no knowledge present)  wrong type / (absent / null when knowledge present)
knowledge.path              string / (absent / null when no knowledge present)  wrong type / (absent / null when knowledge present)
prerequisites               list[str]/ []                                       wrong type/ wrong list type
extra fields                -                                                   forbidden