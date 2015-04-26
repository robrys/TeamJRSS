# TeamJRSS
**Tech@NYU - Event Check-In** (April 24th, 2015)

**Team Members:**
Jessica Johnson, Robert Ryszewski, Mariano Salinas, William Shi

**The Problem:**
  Getting attendees of events properly checked in to the API, with their NYU N#s (if any).

**Our Solution:**

1. Offer an RSVP link on the event page that takes in an email or NYU N#
 * If users have attended any Tech event before, they are then RSVP'd
 * Otherwise, they're prompted to fill out their Name, NYU N#, and Gender

2. At the event, a check-in station can take in either emails or swiped NYU IDs
 * RSVP'd individuals swipe their NYU ID or enter their email, and go in
 * Non-RSVP'd individuals are further prompted for the short, 3 field registration
	
3. After the event, a follow-up email can be sent asking attendees to list their skills for matching with other attendees for future events
 * Email should include a personalized link to update their skills at any time in the future
 * System should periodically send out a reminder every so many weeks/months, as their skills will change

*Please note that this code relies on actual event IDs in the API. Thus "localhost:5000/rsvp" or "localhost:5000/rsvp/100" will not work, but "localhost:5000/541f60e5ff7ba819334c8ffa" for an actual event will.*	

**Design Benefits:**
 * Pre-event RSVP takes care of a good portion of attendees, reducing congestion
 * Already supports ID swiping, which by default would fill in the sole input field on the check-in page
 * NYU students simply swipe and go in, keeps the line moving
 * Only first-time attenders, NYU or not, fill out the brief form
 * Overall, attendees swipe or fill out a single field, minimal complexity/time spent
 
**Design Flexibility:**
 * Under worst case conditions, can make check in page publicly accessible during time of the event
  * Can provide a human-friendly link alias
  * Users can check in on their phones in a distributed manner
 * Multiple check-in stations can be planned in advance for larger events

**Goals for Future Technical Improvement:**
 * Provide a respectable graphical user interface/website design
 * Fix lack of verifying/any security when interacting with the API, done due to dependency problems with Ubuntu
 * Finish only missing functionality in flush_attendees(), which updates the event and its list of attendees on the API
 * Use JS or a similar tool to ensure the fields in the form are filled out, and correctly
  * To ensure API Person object validity, and to prevent unhandled "Bad Request" exceptions in this program
 * Improve general robustness; in particular KeyErrors for user objects that without expected fields
 * Add an "NYU Number" field to Person class in API, make minor adjustments to support it
 * Design logic/system for handling or reducing duplicate emails and Person objects for the same Person
  * Use JS or a similar tool to have the "Email/N#" field persist through the short form, so users can choose to try different emails if they enter an incorrect one

**Performance Improvements:**
 * Currently make_person() creates a person on the API, then downloads the entire user base
  * Unacceptably slow, poor design, done for convenience of coding under time constraints
 * Currently mark_attended() downloads the entire list of attendees, adds the new attendee, and flushes to the API
  * Unacceptably slow, poor design, done for convenience of coding under time constraints 
