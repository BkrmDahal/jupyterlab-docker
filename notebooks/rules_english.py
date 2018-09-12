from datetime import datetime
from collections import Counter
import pandas as pd


def get_date(text):

	"""
	Function to get total amount from text

	Args: 
		text: ''Dataframe''
			Pandas dataframe with columns - 
				- Text - Word
				- conf - Confidence
				- height - Height of word
				- line - Line number of word
				- x0 - Top left x coordinate
				- x2 - Bottom right x coordinate
				- y0 - Top left y coordinate
				- y2 - Bottom right x coordinate
	Returns:
		date_main: First formatted date of the invoice
		text_main: Value in text dataframe for the first invoice date
		dates: ''Dataframe''
			Dataframe of dates in text - 
				- date - Formatted date
				- text - Value in text dataframe
	"""

	d = []
	for i, r in text.iterrows():
		date = {}
		try:
			date['date'] = (datetime.strptime(r.Text, '%d/%m/%y').date())
			date['text'] = r.Text
		except:
			try:
				date['date'] = (datetime.strptime(r.Text, '%d-%m-%y').date())
				date['text'] = r.Text
			except:
				try:
					date['date'] = (datetime.strptime(r.Text, '%d.%m.%Y').date())
					date['text'] = r.Text
				except:
					pass
		if date:  d.append(date)
	dates = pd.DataFrame(d)
	try:
		date_main = str(dates.date.values[0])
		text_main =  dates.text.values[0]
		return date_main, text_main, dates
	except: 
		return None, None, dates

	
	

def get_table(text, dates):

	"""
	Function to get table from text

	Args: 
		text: ''Dataframe''
			Pandas dataframe with columns - 
				- Text - Word
				- conf - Confidence
				- height - Height of word
				- line - Line number of word
				- x0 - Top left x coordinate
				- x2 - Bottom right x coordinate
				- y0 - Top left y coordinate
				- y2 - Bottom right x coordinate
		dates: ''Dataframe''
			Dataframe of dates in text - 
				- date - Formatted date
				- text - Value in text dataframe
	Returns:
		output: Dictionary with important info from the invoice
		idx: Indices of words that are important for total amount
	"""

	try:
		lines = text.loc[text.Text.isin(dates.text)].line.values
	except:
		return pd.DataFrame(), []
	invoices = []
	idx = []
	for line in lines:
		line_df = text.loc[text.line == line].copy()
		invoice = {}
		indices = []
		invoice['Date'], date, _ = get_date(line_df)
		if not date :
			break;
		try:
			reference = line_df.loc[text['Text'].str.contains("^[U]{1}[a-zA-Z0-9]{9}$")].Text.values[0]
			invoice['Reference'] = reference
		except:
			reference = ""
			invoice['Reference'] = None
		try:
			value = line_df.loc[text['Text'].str.contains("\d+(\.\d{1,2})$")].Text.values[0]
			invoice['Value'] = float(value.replace(',',''))
		except:
			value = ""
			invoice['Value'] = None
		extras = line_df.loc[~line_df.Text.isin([date, value, reference])].Text.values
		idx.extend([reference, value])
		idx.extend(extras)
		other = ''
		for extra in extras:
			other += extra + ', '
		invoice['Other'] = other[:-2]
		invoices.append(invoice)

	invoices = pd.DataFrame(invoices)

	idx = text.loc[text.Text.isin(idx)].index

	return invoices, idx


def get_total(text, output):
	"""
	Function to get total amount from text

	Args: 
		text: ''Dataframe''
			Pandas dataframe with columns - 
				- Text - Word
				- conf - Confidence
				- height - Height of word
				- line - Line number of word
				- x0 - Top left x coordinate
				- x2 - Bottom right x coordinate
				- y0 - Top left y coordinate
				- y2 - Bottom right x coordinate
		output: Dictionary with important info from the invoice
	Returns:
		output: Dictionary with important info from the invoice
		idx: Indices of words that are important for total amount
	"""
	lines = [[line, line+1, line+2] for line in text.loc[text.Text.str.lower().str.contains("total")].line.values]   
	amount = []
	idx = []
	for setl in lines:
		for line in setl:
			amount.extend(text.loc[text.line == line].loc[text['Text'].str.contains("\d+(\.\d{0,1,2}){0,1}$")].Text.values)    
	invoice = list(set(amount))    
	idx.extend(invoice)
	inv = []
	for i in invoice:
		try:
			inv.append(float(i.replace(',','')))
		except:
			continue

	invoice = inv
	try:
		val = max(invoice)
	except:
		return output, []

	if val.is_integer():
		try:
			val += max([i for i in invoice if i < 1])
		except:
			pass
	output['Total Amount'] = val
	idx = text.loc[text.Text.isin(idx)].index
	return output, idx
	
def get_receipt(text, output):

	"""
	Function to get payment number from text

	Args: 
		text: ''Dataframe''
			Pandas dataframe with columns - 
				- Text - Word
				- conf - Confidence
				- height - Height of word
				- line - Line number of word
				- x0 - Top left x coordinate
				- x2 - Bottom right x coordinate
				- y0 - Top left y coordinate
				- y2 - Bottom right x coordinate
		output: Dictionary with important info from the invoice
	Returns:
		output: Dictionary with important info from the invoice
		idx: Indices of words that are important for payment number
	"""

	lines = [[line, line+1, line+2] for line in text.loc[(text.Text.str.lower().str.contains("payment")) | (text.Text.str.lower().str.contains("reference"))].line.values]   
	num = []
	idx = []
	for setl in lines:
		for line in setl:
			num.extend(text.loc[text.line == line].loc[text['Text'].str.contains("^[a-zA-Z0-9]{7}\d{2}[a-zA-Z0-9]*$")].Text.values)    

	try:        
		output['Payment No.'] = num[0]
		idx.append(num[0])
	except:
		pass
	idx = text.loc[text.Text.isin(idx)].index
	return output, idx

def account_num(text, output):

	"""
	Function to get account number from text

	Args: 
		text: ''Dataframe''
			Pandas dataframe with columns - 
				- Text - Word
				- conf - Confidence
				- height - Height of word
				- line - Line number of word
				- x0 - Top left x coordinate
				- x2 - Bottom right x coordinate
				- y0 - Top left y coordinate
				- y2 - Bottom right x coordinate
		output: Dictionary with important info from the invoice
	Returns:
		output: Dictionary with important info from the invoice
		idx: Indices of words that are important for account number

	"""

	lines = [[line, line+1, line+2] for line in text.loc[(text.Text.str.lower().str.contains("account")) | (text.Text.str.lower().str.contains("acct"))].line.values]   
	num = []
	idx = []
	for setl in lines:
		for line in setl:
			num.extend(text.loc[text.line == line].loc[text['Text'].str.contains("^\d{4,}$")].Text.values)    
	try:        
		output['Account No.'] = num[0]
		idx.append(num[0])
	except:
		pass
	idx = text.loc[text.Text.isin(idx)].index
	return output, idx	    



def bank_name(text, output):
	"""
	Function to get bank name from text

	Args: 
		text: ''Dataframe''
			Pandas dataframe with columns - 
				- Text - Word
				- conf - Confidence
				- height - Height of word
				- line - Line number of word
				- x0 - Top left x coordinate
				- x2 - Bottom right x coordinate
				- y0 - Top left y coordinate
				- y2 - Bottom right x coordinate
		output: Dictionary with important info from the invoice
	Returns:
		output: Dictionary with important info from the invoice
		idx: Indices of words that are important for bank name

	"""
	lines = []
	idx = []
	for values in [['bank', 'name']]:
		line_ = []
		for value in values:
			l = [line for line in text.loc[(text.Text.str.lower().str.contains(value))].line.values]
			line_.extend(l)
		cnt = Counter(line_)
		lines.extend([k for k, v in cnt.items() if v > 1])
	lines = [[line, line+1, line+2] for line in lines]
	name = []
	for setl in lines:
		for line in setl:
			name.extend(text.loc[text.line == line].loc[text['Text'].str.contains("^[a-zA-Z]{3,}$")].Text.values)    
	try:        
		output['Bank name'] = name[0]
		idx.append(name[0])
	except:
		pass
	idx = text.loc[text.Text.isin(idx)].index
	return output, idx	    



def sort_code(text, output):
	"""
	Function to get sort code from text

	Args: 
		text: ''Dataframe''
			Pandas dataframe with columns - 
				- Text - Word
				- conf - Confidence
				- height - Height of word
				- line - Line number of word
				- x0 - Top left x coordinate
				- x2 - Bottom right x coordinate
				- y0 - Top left y coordinate
				- y2 - Bottom right x coordinate
		output: Dictionary with important info from the invoice
	Returns:
		output: Dictionary with important info from the invoice
		idx: Indices of words that are important for sort code

	"""

	lines = []
	idx = []
	for values in [['bank', 'key'], ['sort', 'code']]:
		line_ = []
		for value in values:
			l = [line for line in text.loc[(text.Text.str.lower().str.contains(value))].line.values]
			line_.extend(l)
		cnt = Counter(line_)
		lines.extend([k for k, v in cnt.items() if v > 1])
	lines = [[line, line+1, line+2] for line in lines]
	code = []
	for setl in lines:
		for line in setl:
			val = text.loc[text.line == line]
			code.extend(val.loc[(text['Text'].str.contains("^\d{6,}$")) | (text['Text'].str.contains("^\d{2}-\d{2}-\d{2}.*$"))].Text.values)    
	try:        
		output['Sort Code'] = code[0]
		idx.append(code[0])
	except:
		pass
	idx = text.loc[text.Text.isin(idx)].index
	return output, idx





def results(text):
	"""
	Function to get important information from text

	Args: 
		text: ''Dataframe''
			Pandas dataframe with columns - 
				- Text - Word
				- conf - Confidence
				- height - Height of word
				- line - Line number of word
				- x0 - Top left x coordinate
				- x2 - Bottom right x coordinate
				- y0 - Top left y coordinate
				- y2 - Bottom right x coordinate
	Returns:
		output: Dictionary with important info from the invoice
		table: Table in invoice
		green_indices: Indices of words that are important in text dataframe

	"""
	output = {}
	green_indices = []
	
	_, _, dates = get_date(text)

	
	try:
		green_indices.extend(text.loc[text.Text.isin(dates.text)].index)
		dates = dates.loc[dates.date != max(dates.date)]
		output['Date'] =  str(max(dates.date))
	except:
		pass
	

	output, idx = get_total(text, output)
	green_indices.extend(idx)
	output, idx = get_receipt(text, output)
	green_indices.extend(idx)
	output, idx = account_num(text, output)
	green_indices.extend(idx)
	output, idx = bank_name(text, output)

	green_indices.extend(idx)
	output, idx = sort_code(text, output)
	green_indices.extend(idx)


	table, idx = get_table(text, dates)
	green_indices.extend(idx)

	return output, table, green_indices


