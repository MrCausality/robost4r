factsXml = ET.parse(commandDir + "facts.xml")
facts = factsXml.getroot()

SQL = SQL.SQL()

if not self.parms:
    fact = SQL.selectAsArray("SELECT * FROM facts ORDER BY RAND()LIMIT 0,1;")
    #self.output = "Fact " + fact[0].text + ": " + fact[1].text
    self.output = fact

elif self.parms[0] == "add":
    factsXml.write(commandDir + "facts.xml")

else:
    for fact in facts:
        
        if fact[0].text == self.parms[0]:
            self.output = fact[1].text
            break
        else:
            self.output = "cant find fact"
