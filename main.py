import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
"""
little python script to plot poll "megapart" done by AGJ-Freiburg

run with: python: main.py
(c) 2022 Robin Haensse
"""



"""
handleTexts: 
    gets an array of textmessages and writes in a file
"""
def handleTexts(question_index, texts):
    with open("results/" + str(question_index) + 'additional_answers.txt', 'w') as f:
        for text in texts:
            f.write(text + "\n")
            f.write("\n\n*********************************************************\n")

"""
plot_checkboxes:
    plots the answers of a question which had multiple options (checkboxes) 
    plots a relative and an absolute bar chart
"""
def plot_checkboxes(question_index, question, answers, preprocessed_data):
    # get the rows from the dataset containing the answers of question with id: question_index
    roi = np.where(preprocessed_data[:, 3] == question_index)
    
    # handle optional text input
    texts = np.asarray(preprocessed[roi, 7][0])
    texts = texts[np.where(texts != "")]
    if len(texts) > 0:
        handleTexts(question_index, texts) 
    
    # PLOT ABSOUTE VALUES
    data_pre = preprocessed[roi, 10::][0]

    res = []
    for dp in data_pre:
        res.append(dp)
    n = len(res)

    res = np.asarray(res).astype(int)
    counts = []
    for x in range(res.shape[1]):
        sum = np.sum(res[:, x])
        counts.append(sum)

    counts = counts[0:len(answers)]
    y_pos = np.arange(len(answers))

    plt.figure((int)(question_index), figsize =(10, 7))    
    plt.bar(y_pos, counts, color=(0.09019608, 0.40784314, 0.69019608, 1))

    # Create names on the x-axis
    plt.xticks(y_pos, answers, rotation=12, horizontalalignment='right', fontsize='x-small')
    yint = range(0, math.ceil(max(counts))+1)
    plt.yticks(yint)
    plt.ylabel("Anzahl der Antworten (absolut)")
    plt.title(question + " n=" +str(n) + ", mehrfachauswahl möglich")

    for i in range(len(counts)):
        plt.text(i, counts[i], counts[i], ha = 'center')

    plt.savefig("results/" + question_index  + "_absolut", dpi=300)
    plt.close()

    # PLOT RELATIVE VALUES
    sum = np.sum(counts)
    percantages = (counts / np.asarray(([n] * len(counts)))) * 100

    plt.figure((int)(question_index)*100, figsize =(10, 7))    
    plt.bar(y_pos, percantages, color=(0.09019608, 0.40784314, 0.69019608, 1))

    # Create names on the x-axis
    plt.xticks(y_pos, answers, rotation=12, horizontalalignment='right', fontsize='x-small')
    yint = range(0, 105, 5)
    plt.yticks(yint)

    for i in range(len(percantages)):
        plt.text(i, percantages[i], str((int)(percantages[i])) + " %", ha = 'center')

    plt.ylabel("Antworten in (relativ)")
    plt.title(question + " n=" +str(n) + ", mehrfachauswahl möglich")
    plt.savefig("results/" + question_index  + "_relative", dpi=300)
    plt.close()


"""
plot_radio:
    plots the answers of a question which had a single option to chooce(radio buttons) 
    plots a relative and an absolute bar chart
"""
def plot_radio(question_index, question, answers, preprocessed_data):
    # get the rows from the dataset containing the answers of question with id: question_index
    roi = np.where(preprocessed_data[:, 3] == question_index)
    data_pre = preprocessed[roi, 1][0]

    # handle optional text input
    texts = np.asarray(preprocessed[roi, 7][0])
    texts = texts[np.where(texts != "")]
    if len(texts) > 0:
        handleTexts(question_index, texts) 
    
    # PLOT ABSOUTE VALUES
    res = []
    for dp in data_pre:
        if((int)(dp) > 0 ) :
           res.append((int)(dp))

    n = len(res)
    counts = []
    res = np.asarray(res)

    for a_ix, a in enumerate(answers):
        counts.append(np.count_nonzero(res == a_ix+1))
    
    y_pos = np.arange(len(answers))

    plt.figure((int)(question_index), figsize =(10, 7))    
    plt.bar(y_pos, counts, color=(0.09019608, 0.40784314, 0.69019608, 1))

    # Create names on the x-axis
    plt.xticks(y_pos, answers, rotation=12, horizontalalignment='right', fontsize='x-small')
    yint = range(0, math.ceil(max(counts))+1)
    plt.yticks(yint)
    plt.ylabel("Anzahl der Antworten (absolut)")
    plt.title(question + " n=" +str(n))

    for i in range(len(counts)):
        plt.text(i, counts[i], counts[i], ha = 'center')

    plt.savefig("results/" + question_index  + "_absolut", dpi=300)
    plt.close()

    # PLOT RELATIVE VALUES
    sum = np.sum(counts)
    percantages = (counts / sum) * 100
    plt.figure((int)(question_index)*100, figsize =(10, 7))    
    plt.bar(y_pos, percantages, color=(0.09019608, 0.40784314, 0.69019608, 1))

    # Create names on the x-axis
    plt.xticks(y_pos, answers, rotation=12, horizontalalignment='right', fontsize='x-small')
    yint = range(0, 105, 5)
    plt.yticks(yint)

    for i in range(len(percantages)):
        plt.text(i, percantages[i], str((int)(percantages[i])) + " %", ha = 'center')

    plt.ylabel("Antworten (relativ)")
    plt.title(question + " n=" +str(n))
    plt.savefig("results/" + question_index  + "_relative", dpi=300)
    plt.close()

# font in CI
font = {'family' : 'Oswald',
        'weight' : 'normal',
        'size'   : 11}
        
matplotlib.rc('font', **font)      

print("Evaluation tool for AGJ FREIBURG Megapart")

# questions indices
radios = [2, 3, 5, 7, 8, 10, 13, 14, 15, 20, 30, 33, 34, 36]
checkboxes = [1, 4, 6, 11, 12, 17, 18, 19, 21, 22, 23, 24, 25, 27, 28, 29, 35]
onlytext = [32, 38]
information = [0, 9, 16, 26, 31, 37, 39]
file = "raw/megapart.csv"

# answers (multiple) from a person (key) which should not be included in the evaluation
removeKeys = ["ZKIpAvUDOEFoCkNJER2pxKulx8wP4n5OxPijiFuoa4lOo1QWINJXcQEUX1wvT5BXNGvbTpXqZpcz0rZd2cTijuFtmmzhFprKvvQ", # p. n. "bitte löschen"
            "4KUqdLUb69WQY4iWEqftg4Z0b1WjxgDLmfhj1dq3G6zgPeF6P0UX096wKmOV9UBhmpyTzIPG59glOo11uMOdXhXR5o4wSoigmIl",  # everthing is 0 and only 5 answers
            "GNa1JEyNFwxMXmoIfnQGWOXA6oHFIthtcWqM2Blcqo4sheIzBeEF5fx3SOSwcfaBCZEVjSV2P9F5ASq15YvjjJWbkDtEEf6HHve"] # "delete me daddy"

## assert if questions indices are correct in total
for i in range(39):
    assert (i in radios or i in checkboxes or i in onlytext or i in information) , "Question logic is off"
assert (len(radios) + len(checkboxes) + len(onlytext) + len(information)) == 40, "Question logic is off (total amount)"
assert (np.sum(radios) + np.sum(checkboxes) + np.sum(onlytext) + np.sum(information)) == ((39 * 40) // 2) , "Question logic is off (indices)"

my_data = np.genfromtxt(file, delimiter='|', dtype=None, names=True)


#  A LINE IN THE DATA LOOKS LIKE THIS
# ['"ID"', '"answer"', '"code"', '"qid"', '"date"', '"agent"', '"ip"', '"text"', '"pollstarted"', '"ref"']
print("There are " + str(len(my_data)) + " rows in the dataset")
print("a row looks like: ", my_data[0])

deleteIx = []
for md_ix, md in enumerate(my_data):
    if md["code"] in removeKeys:
        deleteIx.append(md_ix)

print("Delete... ", len(deleteIx), " answers")
my_data = np.delete(my_data, deleteIx)

print("**" * 100)
print("There are ", len(my_data), " single answers ")
keys = []
for md in my_data:
    if md["code"] not in keys:
        keys.append(md["code"])

print("There were ", len(keys), " different entities (Human who did the poll)")


## PREOPROCESS DATA
preprocessed = []
for md_ix, md in enumerate(my_data): 
    if(md["qid"] in radios):
        md["answer"] = md["answer"].replace("radio/cb: ", "")
        md["ref"] = "radio"
        temp_l = list(md)
        for i in range(25):
            temp_l.append(-1)
        preprocessed.append(tuple(temp_l))

    elif(md["qid"] in checkboxes):
            md["answer"] = md["answer"].replace("radio/cb: ", "")
            number = (int)(md["answer"])
            binary = bin(number)[2:] + ""
            binary = binary[::-1]
            md["ref"] = "checkbox"
            temp_l = list(md)
            for i in range(25):
                answer = 0
                if i < len(binary):
                    answer = binary[i]
                temp_l.append(answer)
            preprocessed.append(tuple(temp_l))

    elif (md["qid"] in onlytext):
            md["answer"] = md["answer"].replace("radio/cb: ", "")
            md["ref"] = "TEXT"
            temp_l = list(md)
            for i in range(25):
                answer = 0
                if i < len(binary):
                    answer = binary[i]
                temp_l.append(answer)
            preprocessed.append(tuple(temp_l))
    else:
        assert False, "should not happen"

preprocessed = np.asarray(preprocessed)

# check nothing is lost in preprocessing step
assert(preprocessed.shape[0] == len(my_data)), "len missmatch"

## preprocessing done
# start plotting the resulsts
ind = np.where(preprocessed[:,3] == "32")
ages_pre = preprocessed[ind, 7][0]
ages_result = []

## Process AGE ###########################
# remove empty lines
for ap in ages_pre:
    if ap != '':
        if (int)(ap) > 0:
            ages_result.append((int)(ap))
ages_result = np.asarray(ages_result)
ages_result = np.asarray(ages_result)
fig = plt.figure(0, figsize =(10, 7))
fig.text(0.5, 0.9, "n=" + str(len(ages_result)), wrap=True, horizontalalignment='center')
plt.boxplot(ages_result, patch_artist=True,  boxprops=dict(facecolor=(0.09019608, 0.40784314, 0.69019608, 1), color=(0.09019608, 0.40784314, 0.69019608, 1)))
plt.ylabel("Alter in Jahren")
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False) # remove buttom axis
plt.savefig( "results/age")

## Process CHECKBOXES ###########################
plot_checkboxes("1", "Wo hast Du die Möglichkeit, ins Internet zu gehen?",  ["in sozialen Einrichtungen", "an öffentlichen Plätzen","in Bibliotheken oder anderen öffentlichen Einrichtungen", "in Cafés, Bars oder Supermärkten", "an meiner Arbeitsstelle", "bei Bekannten oder Freund*innen", "in meiner eigenen Wohnung", "über mobile Daten", "ich nutze kein Internet"], preprocessed)
plot_checkboxes("4", "Welches/welche der folgenden Geräte hast Du in den letzten 2 Wochen benutzt?",  ["Laptop", "Desktop Computer / PC", "Tablet"], preprocessed)
plot_checkboxes("6", "Wo lädst Du den Akku Deiner elektronischen Geräte auf?",  ["in einer sozialen Einrichtung", "an öffentlichen Ladestationen", "in Cafés, Bars oder Supermärkten", "bei meiner Arbeitsstelle", "bei Bekannten oder Freund*innen","in meiner Wohnung",  "weiß ich nicht"], preprocessed)
plot_checkboxes("11", "Verwendest Du einen oder mehrere der folgenden Cloud-Anbieter?", ["Google Drive", "iCloud","Dropbox", "OneDrive","Nextcloud","Reconnect", "Sonstiges", "anderer Anbieter"], preprocessed)
plot_checkboxes("12", "Wem vertraust Du bei technischen Fragen?", ["Sozialarbeiter*innen", "staatlichen Institutionen", "ich informiere mich selbst (z.B. über Google, YouTube, Foren, Bücher)","Bekannten und Freund*innen", "niemandem", "Sonstiges", "andere Person"], preprocessed)
plot_checkboxes("17", "Welche Funktionen wünschst Du Dir für unsere Cloud-Lösung?", ["Kontaktdaten speichern", "Karte mit relevanten Orten (z.B. soziale Einrichtungen, Ärzte, Ämter)", "Teilen von Dokumenten",  "Verschlüsseln der Dateien und Dokumente", "Hoch- und Herunterladen von eigenen Dokumenten", "Kalender (z.B. für Erinnerungen an Termine)", "Chat mit Sozialarbeiter*innen", "Chat mit Bekannten und Freund*innen", "Sonstiges", "andere Funktion"], preprocessed)
plot_checkboxes("18", "Welche Daten würdest Du in der Cloud speichern?", ["Anträge oder Schreiben an Behörden", "Briefe von Behörden", "Briefe von Freund*innen", "Fotos", "persönliche Dokumente (z.B. Personalausweis)", "Sonstiges",  "eigene Angabe", "gar nichts"], preprocessed)
print("25%")
plot_checkboxes("19", "Aus welchem Grund möchtest Du keine Dokumente hoch- und herunterladen können?", ["ich weiß nicht, was das bedeutet",  "ich habe Datenschutzbedenken", "das ist mir zu viel Aufwand", "ich sehe keinen Mehrwert darin", "Sonstiges", "anderer Grund"], preprocessed)
plot_checkboxes("21", "Wem würdest Du die Dokumente in der Cloud freigeben?", ["sozialen Einrichtungen", "einzelnen Sozialarbeiter*innen", "Behörden (z.B. Arbeitsamt, Anwohnermeldeamt)", "Krankenkassen", "Bekannten und Freund*innen", "Sonstiges", "andere Person / Institution"], preprocessed)
plot_checkboxes("22", "Wenn Du Dein Passwort für die Cloud vergessen hast, wie möchtest Du es wiederbekommen?", ["Wiederherstellung per SMS", "Wiederherstellung per E-Mail", "Sozialarbeiter*innen sollen mir ein neues Passwort erstellen", "Sonstiges","anderer Weg"], preprocessed)
plot_checkboxes("23", "Welchen Zugriff sollten Sozialarbeiter*innen nach Absprache mit Dir auf Deine Daten in der Cloud haben?", ["meine Dokumente ansehen", "meine Dokumente bearbeiten","neue Dokumente von mir hochladen", "Sonstiges", "eigene Angabe"], preprocessed)
plot_checkboxes("24", "Wer sollte die Cloud betreiben?", ["soziale Einrichtungen (z.B. Caritas, Diakonie, Tafel, die Kirche)", "Bildungsstätten (z.B. Schulen, Hochschulen, Universitäten)", "private Firmen (z.B. Microsoft, Telekom, SAP)", "das ist mir egal", "weiß ich nicht", "Sonstiges", "andere*r Betreiber*in"], preprocessed)
plot_checkboxes("25", "Angenommen, Du hast ein Problem bei der Nutzung unserer Cloud. Auf welchem Weg möchtest Du unterstützt werden?", ["Support-Telefonnummer", "Livechat", "Hilfeseite der Cloud", "Sozialarbeiter*in", "Begleitheft aus Papier", "Bekannte und Freund*innen", "ich recherchiere selbst im Internet", "sonstiges", "anderer Weg",", answers, preprocessed"], preprocessed)
plot_checkboxes("27", "Welche Dokumente besitzt Du?", ["Personalausweis","Krankenkarte", "Reisepass", "Geburtsurkunde", "Sonstiges", "andere Dokumente", "keins der Genannten"], preprocessed)
plot_checkboxes("28", "Zu welchen dieser Dokumente hast Du noch Zugang?", ["Personalausweis", "Krankenkarte","Reisepass","Geburtsurkunde", "zu keinem der Aufgeführten"], preprocessed)
plot_checkboxes("29", "Wo bewahrst Du diese Dokumente auf?", ["in meinem Geldbeutel", "in meinem Mantel oder Rucksack", "in einem Versteck", "digital auf einem Datenspeicher (z.B. USB-Stick, Festplatte, Smartphone, Laptop, Cloud)", "in einer sozialen Einrichtung", "bei Bekannten oder Freund*innen",  "Sonstiges", "Dein Aufbewahrungsort", "möchte ich nicht beantworten"], preprocessed)
plot_checkboxes("35", "Wo übernachtest Du im Moment am meisten?", ["draußen", "in sozialen Einrichtungen (z.B. Notunterkunft, )", "in meiner eigenen Wohnung", "im Zelt, Wohnwagen, Campingplatz, in einer Gartenlaube oder Ähnlichem", "bei meiner Arbeitsstelle",  "in Treppenhäusern, Kellern oder Dachböden", "bei Bekannten oder Freund*innen", "bei meinen Eltern", "sonstiges", "anderer Ort", "möchte ich nicht beantworten"], preprocessed)
print("50%")

## Process RADIO BUTTONS ###########################
plot_radio("2", "Was für ein Handy besitzt Du?", ["Tastenhandy", "iPhone", "anderes Smartphone", "ich besitze kein Handy", "weiß ich nicht"], preprocessed)
plot_radio("3", "Wie viel Datenvolumen für mobiles Internet steht Dir monatlich zur Verfügung?", ["weniger als 2 Gigabytes",  "2-10 Gigabytes",  "mehr als 10 Gigabytes", "weiß ich nicht"], preprocessed)
plot_radio("5", "Gehst Du mehrmals pro Woche in eine soziale Einrichtung?", ["ja", "nein", "weiß ich nicht"], preprocessed)
plot_radio("7", "Gibt es in der sozialen Einrichtung, in der Du am meisten bist, ein freies WLAN?", ["ja", "nein", "weiß ich nicht"], preprocessed)
plot_radio("8", "Wie gut funktioniert das WLAN in der Einrichtung?", ["es funktioniert einwandfrei", "es funktioniert eher gut", "es funktioniert eher schlecht", "es funktioniert überhaupt nicht"], preprocessed)
print("75%")
plot_radio("10", "Wie vertraut bist Du mit bestehenden Cloud-Lösungen?", [       "sehr vertraut",       "eher vertraut",       "eher nicht vertraut",       "gar nicht vertraut",       "weiß ich nicht"], preprocessed)
plot_radio("13", "Hast Du die Möglichkeit, analoge Dokumente zu digitalisieren? Wie umfangreich machst Du das?",  ["alles", "ca. die Hälfte",  "nur das Wichtigste", "gar nichts", "weiß ich nicht"], preprocessed)
plot_radio("14", "Hast Du eine eigene E-Mail-Adresse, zu der Du Zugang hast", ["ja","nein","weiß ich nicht"], preprocessed)
plot_radio("15", "Wie häufig schaust Du in etwa in Dein E-Mail-Postfach?", ["täglich", "wöchentlich", "monatlich", "jährlich"], preprocessed)
plot_radio("20", "Würdest Du digitale Dokumente, die in der Cloud abgelegt sind, temporär anderen Leuten freigeben?", ["ja, ich würde meine Dokumente teilen", "nein, ich möchte die einzige Person sein, die Zugriff auf meine Daten hat", "ich verstehe nicht, was Freigabe bedeutet", "Sonstiges"], preprocessed)
plot_radio("30", "Wie oft hast Du Probleme mit verlorenen Dokumenten?", ["nie", "selten", "eher öfter", "häufig", "fast immer", "weiß ich nicht"], preprocessed)
plot_radio("33", "Welchem Geschlecht fühlst Du Dich zugehörig?", ["weiblich", "männlich", "divers", "möchte ich nicht beantworten"], preprocessed)
plot_radio("34", "Wie ist Deine Wohnsituation?", ["ich bin aktuell obdachlos", "ich bin aktuell wohnungslos", "ich bin von Wohnungslosigkeit bedroht", "ich war wohnungslos, bin es aber nicht mehr", "ich bin nicht wohnungslos und war es nie", "möchte ich nicht beantworten"], preprocessed)
plot_radio("36", "Was ist Deine Muttersprache?", ["Deutsch", "Russisch",  "Türkisch", "Polnisch", "Italienisch", "Englisch", "Spanisch", "Griechisch", "Rumänisch", "Französisch", "sonstiges", "andere Sprache", "möchte ich nicht beantworten"], preprocessed)
print("90%")

# the last question was a place for a feedback (only text)
roi = np.where(preprocessed[:,3] == "38")
texts = preprocessed[roi, 7][0]
texts = texts[np.where(texts != "")]
handleTexts("38", texts)
print("100%")

print("*" * 80)
print(" OK " * 20)
print("*" * 80)
