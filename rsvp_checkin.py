from flask import Flask, request, render_template
import requests, json
import os

app = Flask(__name__)
rsvp_list=[]
user_base={}
attendees=[]

def rsvpd(email_addr):
	return email_addr in rsvp_list

def mark_attended(email_addr, tn_event):
	# make sure you have the most up to date attendees list
	print attendees
	load_attendees(tn_event)
	attending_user=person_exists(email_addr)
	attendees.append(attending_user)
	# update the attendees list on the API
	# flush_attendees()

def add_rsvp(email_addr):
	global user_base, rsvp_list
	# this fails if any user objects created without a contact/email field
	for people in user_base['data']:
		print people['contact']['email']
		if '@' in email_addr:
			if( people['contact']['email'] == email_addr ):
				rsvp_list.append(people)
		else: # this will be for nyu_id field
			if(people['id'] == email_addr):
				rsvp_list.append(people)
	# serious error if user not in user base, even after created

def make_person(name, nyu_num, gender, email_addr):
	global user_base
	# would add nyu_num as well if the field existed
	data = { 'data' : {'type':'people', 'name': name, 'gender':gender, 'contact': {'email': email_addr} } }
	payload=json.dumps(data)
	headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'x-api-key': 'uCl5Eg3Morm4alT7Y'}
	r = requests.post("https://api.tnyu.org/v2-test/people", headers=headers, verify=False, data=payload)
	user_base.clear()
	load_database()

@app.route("/rsvpd/<tn_event>", methods=['GET', 'POST'])
@app.route("/checked_in/<tn_event>", methods=['GET', 'POST'])
def proc_form(tn_event):
	make_person(request.form['name'], request.form['nyu_num'], request.form['gender'], request.form['email'])
	add_rsvp(request.form['email'])
	if(request.form['checking_in'] == "True") : 
		mark_attended(request.form['email'], tn_event)
		checking_in=True
	else: checking_in=False
	return render_template('rsvp_checkin.html', checking_in=checking_in, done=True)

# now can easily have a custom page for each event being RSVP'd to
@app.route("/rsvp/<tn_event>", methods=['GET', 'POST'])
def process_user(tn_event, checking_in=False):
	# email/NYU ID has been submitted
	if( request.method == 'POST'): 
		# if they are on the rsvp list, they are done
		if( rsvpd(request.form['email']) ):
			if(request.form['checking_in']=="True") : mark_attended(request.form['email'], tn_event)
			return render_template('rsvp_checkin.html', checking_in=checking_in, done=True, tn_event=tn_event)
		# if they exist as a person, add them to the rsvp list
		elif (person_exists(request.form['email'])!=False): 
			add_rsvp( request.form['email'] )
			if(request.form['checking_in']=="True") : mark_attended(request.form['email'],tn_event )
			return render_template('rsvp_checkin.html', checking_in=checking_in, done=True, tn_event=tn_event)
		# if they don't exist as a person and haven't rsvp'd, fill out the fields
		else:
			return render_template('rsvp_checkin.html', checking_in=checking_in, current_state="fillout_form", email_addr=request.form['email'], tn_event=tn_event)
	# email/NYU ID has not been submitted, only starting rsvp/checkin
	return render_template('rsvp_checkin.html', checking_in=checking_in, current_state="start", tn_event=tn_event)

def load_attendees(tn_event):
	global attendees
	headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'x-api-key': 'uCl5Eg3Morm4alT7Y'}
	r = requests.get('https://api.tnyu.org/v2-test/events/%s' %(tn_event), headers=headers,verify = False)
	event_obj = json.loads(r.text)
	del attendees[:]
	for people in event_obj['data']['links']['attendees']['linkage']:
		attendees.append(people['id'])

def load_database():
	global user_base
	headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'x-api-key': 'uCl5Eg3Morm4alT7Y'}
	r = requests.get('https://api.tnyu.org/v2-test/people', headers=headers,verify = False)
	user_base = json.loads(r.text)

# no logic for handling duplicate emails for same user
def person_exists(email_addr):
	global user_base
	# this fails if any user objects created without a contact/email field
	for people in user_base['data']:
		print people['contact']['email']
		if '@' in email_addr:
			if( people['contact']['email'].lower() == email_addr.lower() ):
				return True
				# return people['id']
		else: # this will be for future nyu_id field
			if(people['id'] == email_addr):
				return True
				# return people['id']
	return False

@app.route("/checkin/<tn_event>", methods=['GET', 'POST'])
def checkin(tn_event):
	return process_user(tn_event, True)

if __name__ == "__main__":
	load_database()
	app.run(debug=True)