from dbStuff import classDbStuff
import datetime
import random

class enterStuff(object):

    def dataFields(self):
        dataFields = {
            'trustee_sale_date': {
                'input_type': 'radio',
                'default': 'blank',
                'data_choices': self.firstTuesdays(),
                'max_length': 19
            },
            'county': {
                'input_type': 'radio',
                'default': 'blank',
                'data_choices': ['McLennan','Williamson','Travis','Harris'],
                'max_length': 19
            },
            'foreclosure_type': {
                'input_type': 'radio',
                'default': 'blank',
                'data_choices': ['bank mortgage','private lender','reverse mortgage','hoa/condo'],
                'max_length': 64
            },
            'legal_block': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 25
            },
            'legal_lot': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 25
            },
            'legal_subdivision': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 64
            },
            'deed_of_trust_year': {
                'default': 'blank',
                'input_type': 'radio',
                'data_choices': [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021],
                'max_length': 4
            },
            'original_loan_amount': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 10
            },
            'borrower_name': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 255
            },
            'owner_name': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 255
            },
            'greeting': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 255
            },
            'property_address': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 255
            },
            'market_value': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 10
            },
            'owner_mailing1': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 255
            },
            'owner_mailing2': {
                'default': 'blank',
                'input_type': 'text',
                'max_length': 255
            },
            'status':{
                'default': 'incomplete',
                'input_type': 'radio',
                'data_choices': ['complete','incomplete'],
                'max_length': 10
            }
        }
        return dataFields

    def firstTuesdays(self):
        firstTuesdays = []
        iYear = datetime.datetime.now().year
        iMonth = datetime.datetime.now().month
        if iMonth - 3 < 0:
            iMonth = iMonth - 3 + 12
            iYear = iYear - 1
        else:
            iMonth = iMonth - 3
        i = 0
        while i < 6:
            day = datetime.date(iYear,iMonth,1)
            d = day.weekday()
            offset = 1-d
            if offset < 0: offset = offset + 7
            day = day + datetime.timedelta(offset)
            day = str(day)
            firstTuesdays.append(day)
            if iMonth == 12:
                iMonth = 1
                iYear = iYear + 1
            else:
                iMonth = iMonth + 1
            i = i + 1
        return firstTuesdays

    def pickRandomDoc(self,workingUser):
        dbStuff = classDbStuff()
        listOfIncompleteDocs = dbStuff.getListIncompleteDocuments(workingUser)
        if len(listOfIncompleteDocs) == 0: return None
        return random.choice(listOfIncompleteDocs)[0]

    def getNextFieldToEnter(self,docnum):
        obDbStuff = classDbStuff()
        fields = self.dataFields()
        for f in fields:
            if obDbStuff.checkIfBlank(docnum,f) == "blank":
                return f
        return "status"

    def getDataForDoc(self,docnum):
        dbStuff = classDbStuff()
        ddd = {}
        eee = dbStuff.getDataSingleDoc(docnum)
        for e in eee:
            ddd[e['field_name']] = e['data']
        return ddd        

